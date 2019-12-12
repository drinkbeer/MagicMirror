import cv2
import numpy as np
from numpy import dot
from numpy.linalg import norm
import glob
from os.path import relpath, join

import tensorflow as tf
from tensorflow.python.platform import gfile

def load_model(model_path, input_args, output_args): 
    '''Load the frozen graph ''' 
    model = ImportGraph(model_path) 
    input_args = input_args.split(',') 
    output_args = output_args.split(',') 
    for arg in input_args: 
        model.add_input(arg) 
    for arg in output_args: 
        model.add_output(arg) 
    return model

def resize_imgs(imgs, image_shape): 
    '''Transform the image for the network input Return: ''' 
    resized_imgs = [] 
    for img in imgs: 
        resized_imgs.append(cv2.resize(img, image_shape)) 
    return resized_imgs

def get_cosine_similarity_score(img0, img1):
    '''Return similarity score by cosine similarity '''
    return dot(img0, img1)/(norm(img0)*norm(img1))

def rank_similarity(upload_img_feature, imgs_features, top_n):
    similarities = []
    for img_feature in imgs_features:
        similarities.append(get_cosine_similarity_score(upload_img_feature, img_feature))
    print(similarities)
    return np.array(similarities)

def get_top_n_similar(model_path='./media/resource/frozen_inference_graph.pb', 
                        output_args='import/resnet_v2_50/block3/unit_6/bottleneck_v2/shortcut/MaxPool:0,import/resnet_v2_50/pool5:0',
                        images_dir='../../../Desktop/imgs/*.png', img_dir='', upload_img_path='../../../Desktop/coat_red_0.png', top_n=None):
    fe = FeatureExtractor(model_path=model_path, output_args=output_args)
    images = []
    images_path = []

    for filepath in glob.glob(images_dir):
        images.append(cv2.imread(filepath))
        images_path.append(relpath(filepath, img_dir))
    features0, features1 = fe.run(img=images)    
    features_shallow = np.squeeze(features0).reshape(len(images),-1)
    features_deep = np.squeeze(features1).reshape(len(images),-1)
    
    upload_img = cv2.imread(upload_img_path)
    features0, features1 = fe.run(img=upload_img[None,...])
    upload_feature_shallow = np.squeeze(features0).reshape(-1)
    upload_feature_deep = np.squeeze(features1).reshape(-1)
    similarities_shallow = rank_similarity(upload_feature_shallow, features_shallow, len(images))
    similarities_deep = rank_similarity(upload_feature_deep, features_deep, len(images))
    rank_indices = (similarities_deep).argsort()[:top_n][::-1]
    return [images_path[index] for index in rank_indices]

class ImportGraph(): 
    """ Importing and running isolated TF graph """ 
    def __init__(self, graph_path): 
        # Create local graph and use it in the session 
        self.graph = tf.Graph() 
        config = tf.ConfigProto(allow_soft_placement=True, log_device_placement=False) 
        # config.gpu_options.allocator_type = 'BFC' 
        self.sess = tf.Session(config=config, graph=self.graph) 
        self.input_tensor = [] 
        self.output_tensor = [] 
        with self.graph.as_default(): 
            self.load_graph(graph_path)

    def load_graph(self, graph_path): 
        '''Load the frozen graph ''' 
        if tf.gfile.IsDirectory(graph_path): 
            file_name = "frozen_inference_graph.pb" 
            graph_filename = os.path.join(graph_path, file_name) 
        else: 
            graph_filename = graph_path 
        # Create a graph def object to read the graph 
        with tf.gfile.GFile(graph_filename, "rb") as f: 
            graph_def = tf.GraphDef() 
            graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def)

    def run(self, *args): 
        """ Running the model previously imported """ 
        return self.sess.run(self.output_tensor, feed_dict={input_tensor: data for input_tensor,data in zip(self.input_tensor, args)})

    def add_input(self, tensor_name): 
        self.input_tensor.append(self.graph.get_tensor_by_name(tensor_name))

    def add_output(self, tensor_name): 
        self.output_tensor.append(self.graph.get_tensor_by_name(tensor_name))

class FeatureExtractor(): 
    def __init__(self, model_path, img_shape=(224,224), input_args='import/image_tensor:0', output_args='import/resnet_v2_50/pool5:0'): 
        self.model = load_model(model_path, input_args, output_args)
        self.img_shape = tuple(img_shape)

    def run(self, img): 
        # if img.ndim != 4: 
        #     AssertionError('The input shape of the FeatureExtractor should be 4 dims!!!') 
        if len(img) == 0: 
            print('Warning: No uploaded image!!!') 
            return None 
        return self.model.run(resize_imgs(img, self.img_shape)) 