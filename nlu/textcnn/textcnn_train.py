#coding:utf-8
import torch
import torch.optim as optim
from textcnn_model import TextCNN
from data_loader import build_dataset, calcu_class_weights, batch_generator, config
from textcnn_train_helper import init_network, train_model
import numpy as np
import os
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"


""" 统计模型的参数 """
def count_params(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

""" 设置随机数种子 """
def set_manual_seed(seed):
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True

""" 模型训练 """
def train(config):
    
    set_manual_seed(10)
    
    """ 1: 划分数据集并保存 """
    print("Preparing the batch data ... \n")
    build_dataset(config)
    
    """ 2：计算类别权重，缓解类别不平衡问题 """
    class_weights = calcu_class_weights(config)
    config.class_weights = class_weights
    
    
    """ 3: 划分数据集和生成batch迭代器 """
    train_iter, valid_iter, test_iter = batch_generator(config)
    
    """ 5：模型初始化 """
    print("Building the textcnn model ... \n")
    model = TextCNN(config)
    print(f'The model has {count_params(model):,} trainable parameters\n')
    
    model.to(config.device)
    
    """ 6：开始训练模型 """
    print("Start the training ... \n")
    init_network(model)
    train_model(config, model, train_iter, valid_iter, test_iter)

if __name__ == "__main__":
    train(config)