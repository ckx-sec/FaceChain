import os
import pprint
import sys
import time
from argparse import Namespace
from typing import List

import dlib
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.function_base import append
import torch
import torchvision.transforms as transforms
from PIL import Image

matplotlib.use('Agg')
sys.path.append(".")
sys.path.append("..")

# os.environ["CUDA_VISIBLE_DEVICES"] = '0'

from datasets import augmentations

from IPython.display import display

from models.psp import pSp
from utils.common import log_input_image, tensor2im
# Step 1: Select Experiment Type
experiment_type = 'ffhq_encode'   

# Step 2: Download Pretrained Models 
CODE_DIR = '/home/bandr/ywy/encode--pixel2style2pixel-master/pixel2style2pixel-master/content/pixel2style2pixel'   
def get_download_model_command(file_id, file_name):
    """ Get wget download command for downloading the desired model and save to directory ../pretrained_models. """
    current_directory = os.getcwd()
    save_path = os.path.join(os.path.dirname(current_directory), CODE_DIR, "pretrained_models")
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    url = r"""wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id={FILE_ID}' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id={FILE_ID}" -O {SAVE_PATH}/{FILE_NAME} && rm -rf /tmp/cookies.txt""".format(FILE_ID=file_id, FILE_NAME=file_name, SAVE_PATH=save_path)
    return url

#下载psp_ffhq_encode.pt
MODEL_PATHS = {
    "ffhq_encode": {"id": "1bMTNWkh5LArlaWSc_wa8VKyq2V42T2z0", "name": "psp_ffhq_encode.pt"},
    "ffhq_frontalize": {"id": "1_S4THAzXb-97DbpXmanjHtXRyKxqjARv", "name": "psp_ffhq_frontalization.pt"}
}

path = MODEL_PATHS[experiment_type]
download_command = get_download_model_command(file_id=path["id"], file_name=path["name"])

#下载
#!wget {download_command}

# Step 3: Define Inference Parameters
import torchvision.transforms as transforms

EXPERIMENT_DATA_ARGS = {
    "ffhq_encode": {
        "model_path": "pretrained_models/psp_ffhq_encode.pt",
        "image_path": "notebooks/images/input_img.jpg",
        "transform": transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])
    },
    "toonify": {
        "model_path": "pretrained_models/psp_ffhq_toonify.pt",
        "image_path": "notebooks/images/input_img.jpg",
        "transform": transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])
    },
}
EXPERIMENT_ARGS = EXPERIMENT_DATA_ARGS[experiment_type]   #实验类型

#验证模型是否成功下载
if os.path.getsize(EXPERIMENT_ARGS['model_path']) < 1000000:
  raise ValueError("Pretrained model was unable to be downlaoded correctly!")

# Step 4: Load Pretrained Model
model_path = EXPERIMENT_ARGS['model_path']
ckpt = torch.load(model_path, map_location='cpu')

opts = ckpt['opts']
print("The following is opts")
pprint.pprint(opts)
print("The Above is opts")

# 从这里到json.dump是新加的加解密
n=13 #just used to generate z
from feature_matrix_processing.inner_product_encryption import ImageFeatureIPE
import pickle
#msks=[]
mpks=[]
keys=[]
for _ in range(n):
    app = ImageFeatureIPE(512, g=1.0001)
    keys.append(app)
    #msks.append(app.msk)
    mpks.append(app.mpk)
z=mpks
z = ImageFeatureIPE(512, g=1.0001).padding(z,r=7,n=512-len(z))
pickle.dump(keys,open('keys.pickle','wb'))
pickle.dump(keys,open('keys.pickle.tmp','wb'))
import json
json.dump(z,open(f'z.json','w'))


# update the training options
opts['checkpoint_path'] = model_path
if 'learn_in_w' not in opts:
    opts['learn_in_w'] = False
if 'output_size' not in opts:
    opts['output_size'] = 1024
    

opts = Namespace(**opts)
net = pSp(opts)
net.eval()
net.cuda()
print('Model successfully loaded!')

# Step 5: Visualize Input  调整图像大小
image_path = EXPERIMENT_DATA_ARGS[experiment_type]["image_path"]
original_image = Image.open(image_path)
if opts.label_nc == 0:
    original_image = original_image.convert("RGB")
else:
    original_image = original_image.convert("L")

original_image.resize((256, 256))

#图像对齐
def run_alignment(image_path):
  from scripts.align_all_parallel import align_face
  predictor = dlib.shape_predictor('/home/bandr/ywy/encode--pixel2style2pixel-master/pixel2style2pixel-master/notebooks/shape_predictor_68_face_landmarks.dat')
  aligned_image = align_face(filepath=image_path, predictor=predictor) 
  print("Aligned image has shape: {}".format(aligned_image.size))     #Aligned image has shape: (256, 256)
  return aligned_image

if experiment_type not in ["celebs_sketch_to_face", "celebs_seg_to_face"]:
  input_image = run_alignment(image_path)
else:
  input_image = original_image

input_image.resize((256, 256))
#display(input_image)     #输出的图片是image准备的图片
#input_image.show()

# Step 6: Perform Inference
def run_on_batch(inputs, net, latent_mask=None):
    if latent_mask is None:
        result_batch = net(inputs.to("cuda").float(), randomize_noise=False)
    else:
        result_batch = []
        for image_idx, input_image in enumerate(inputs):
            # get latent vector to inject into our input image
            vec_to_inject = np.random.randn(1, 512).astype('float32')
            _, latent_to_inject = net(torch.from_numpy(vec_to_inject).to("cuda"),
                                      input_code=True,
                                      return_latents=True)
            # get output image with injected style vector
            res = net(input_image.unsqueeze(0).to("cuda").float(),
                      latent_mask=latent_mask,
                      inject_latent=latent_to_inject)
            result_batch.append(res)
        result_batch = torch.cat(result_batch, dim=0)
    return result_batch


# Extract and Save the Images
def get_download_images_command(file_id, file_name):
    """ Get wget download command for downloading the inversion images and save to directory ./inversion_images. """
    save_path = os.getcwd()
    url = r"""wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id={FILE_ID}' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id={FILE_ID}" -O {SAVE_PATH}/{FILE_NAME} && rm -rf /tmp/cookies.txt""".format(FILE_ID=file_id, FILE_NAME=file_name, SAVE_PATH=save_path)
    return url

inversion_images_id = "1wfCiWuHjsj3oGDeYF9Lrkp8vwhTvleBu"
inversion_images_file_name = "inversion_images.zip"
# save_path = "./inversion_images"
save_path = "./yqw_test_image"
# save_path = "./yqw"
download_command = get_download_images_command(inversion_images_id, inversion_images_file_name)

#下载图片
# !wget {download_command}
# !mkdir {save_path}
# !unzip {inversion_images_file_name}



# Visualize the Images
image_paths = [os.path.join(save_path, f) for f in os.listdir(save_path) if f.endswith(".png")]
print(os.listdir(save_path))
list.sort(image_paths)
print("image_paths:")
print(image_paths)
n_images = len(image_paths)

images = []
n_cols = np.ceil(n_images / 2)
fig = plt.figure(figsize=(20, 4))
for idx, image_path in enumerate(image_paths):
    ax = fig.add_subplot(2, n_cols, idx + 1)
    img = Image.open(image_path).convert("RGB")
    images.append(img)
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.imshow(img)
plt.savefig('/home/bandr/ywy/encode--pixel2style2pixel-master/pixel2style2pixel-master/output_image/output')
#plt.show()
print("picture ok")

#Run Inference
img_transforms = EXPERIMENT_ARGS['transform']
transformed_images = [img_transforms(image) for image in images]

batched_images = torch.stack(transformed_images, dim=0)    #把图片放到一个批次里

with torch.no_grad():
    tic = time.time()
    result_images = run_on_batch(batched_images, net, latent_mask=None)
    # print("result_images_befoer的维度为{}" .format(result_images.dim()))    #result_images_befoer的维度为4,result_images_before形状为torch.Size([13, 3, 256, 256])
    # print("result_images_before形状为{}" .format(result_images.shape))
    toc = time.time()
    print('Inference took {:.4f} seconds.'.format(toc - tic))

# Visualize Results


couple_results:List[Image.Image] = []
i = 0
# plt.cla()
for original_image, result_image in zip(images, result_images):
    result_image = tensor2im(result_image)        
    # print("result_images的维度为{}" .format(result_images.dim()))          #变化后的图形仍然是四维，[13, 3, 256, 256]
    # print("result_images形状为{}" .format(result_images.shape))
    res = np.concatenate([np.array(original_image.resize((256, 256))),
                          np.array(result_image.resize((256, 256)))], axis=1)    #连接数组内容
    # print("res形状为{}" .format(res.shape))                                    ##res形状为(256, 512, 3)
    res_im = Image.fromarray(res)        #实现array到image的转换
    # filename = 'Fig'+str('%03d' % i)
    # plt.savefig('/home/bandr/ywy/encode--pixel2style2pixel-master/pixel2style2pixel-master/output_image/'+filename,dpi=350)
    # plt.cla()
    # i+=1
    couple_results.append(res_im)
    display(res_im)
    #res_im.show()

for i in range(len(couple_results)):
    couple_results[i].save(f'testresult{i}.png')

# print(len(couple_results))
# for i in range(len(couple_results)):
#     filename = 'Fig'+str('%03d' % i)
#     print(filename)
#     plt.savefig('/home/bandr/ywy/encode--pixel2style2pixel-master/pixel2style2pixel-master/output_image/'+filename,dpi=350)
#     plt.clf()

