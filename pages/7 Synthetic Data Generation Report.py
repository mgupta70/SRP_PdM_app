import streamlit as st

st.title('''Hydropower Turbine Defect Image Synthesis using Stable Diffusion with ControlNet Reference-only.''')

st.markdown('''
### Abstract
The operation of hydropower turbines involves water flowing at high velocities,
which can cause blade damage, including erosion, pitting, cavitation, and frosting. 
The turbine inspections are critical for maintaining the safety, efficiency, and longevity 
of turbines. However, traditional inspection methods pose significant risks to human inspectors 
due to dangerous working conditions and the challenging environment within the turbines. 
This study proposes a novel approach to enhance turbine blade inspections by leveraging computer 
vision and generative AI techniques to create synthetic damage images. The basic data augmentation
techniques were first performed and achieved a 4.1\% improvement in model performance. By further 
using Stable Diffusion with ControlNet reference-only methods, this approach generates diverse and
high-quality synthetic images, addressing the limitations of basic data augmentation techniques with 
achieved a 6.3\% improvement in model performance. The results demonstrate that the integration of advanced generative
techniques significantly enhances the damage detection system’s performance, offering a safer and more efficient 
solution for hydropower turbine blade inspections.

### Dataset

The existing real dataset in this study are 62 damage images captured on hydropower turbine blades surface during previous inspections. 
The hydropower turbine is located in a south western city in US. 
The images were collected from 2016 to 2023 using digital camera. 
The size of images were varied and the ratio of damage were also diverse, 
the width of images ranges from 320 to 1152 and height ranges from 266 to 1088 pixel.

### Instance Segmentation Model

A YOLOv8 instance segmentation model was trained to automatically localize the damages. 
The YOLOv8 model was chosen for its ability to strike an ideal balance between accuracy and speed, 
achieving a well-calibrated equilibrium. 
The model's anchor-free design and the decision to disable mosaic augmentation during the final training epochs further enhanced its performance.
The hyperparameters used for training included a 0.001 learning rate, 8 batch size, and 100 epochs. 
The dataset was divided into two distinct sets, with 43 images (70%) assigned for training, and 19 images (30%) for validation individually.
The training process lasted approximately one hour using an NVIDIA RTX A4000 GPU and Windows 11 operating system for environment configuration.

### Synthetic Damage Image Generation

Result from the limited real image dataset, 
this section illustrates two methods to increase the training set size. 
The first one is basic data augmentation method which is geometric transformation on 
original image. The second one is using more advanced generative architecture, 
stable diffusion with ControlNet reference-only approach.

### Basic Data Augmentation

A small dataset can lead to overfitting, 
where a model performs well on training data but poorly on new data, 
reducing its generalizability and transferability. 
Basic data augmentation techniques is a standard solution to enlarge dataset with low computation expense and time.
The techniques implement geometric transformation with randomly mixed including scaling, flipping, shearing and rotation as shown in Fig. 1.''')

st.image("media/augmentation.png", caption="Fig 1. Damage image augmentation examples.") 

st.markdown('''The augmented image dimension is identical with its original image dimension.

### Stable Diffusion with ControlNet for Damage Image Synthesis

The concept of a diffusion model for generating new images involves iteratively adding 
noise to an image sample through a diffusion process and then gradually learning to reverse 
this noise step by step through denoising. Stable Diffusion is a variant of the diffusion model 
that enhances efficiency in generating high-quality images by operating within the latent space
of robust pretrained autoencoders. The ControlNet is a neural network architecture to control stable
diffusion models by adding extra conditions. The condition user indicated are setting to trainable part 
and other parts are not trainable. The option of conditions include canny edge maps, depth maps, 
pose estimation, scribbles, segmentation maps, textual descriptions, normal maps, and reference images. 
The reference-only preprocessor is selected in this study to perform image-to-image translation guiding 
by using original images as reference. The synthetic image examples are shown in Fig. 2.''')

st.image("media/synthetic.png", caption="Fig 2. Synthetic image example. (a) Real image; (b) Synthetic image.")

st.markdown('''These synthetic images showcase a diverse range of lighting conditions, as well as variations in the shape, size, and quantity of damages. 
This diversity enhances the model's adaptability and generalizability, effectively compensating for the limitations of the original real images.

### Experiments and Results
This section presents the changes of damage detection model performance after adding basic data augmented images and synthetic images. 
The model behaviors were further analyzed by damage cover area ratio and the number of damages in the training set.
   
### Adding Synthetic Data Strategy and Model Performance
The strategy to add basic augmented data and synthetic data is shown in Fig. 3.''')

st.image("media/workflow.png", caption="Fig 3. mAP for damage detection with the increase of training set size.")

st.markdown('''The experiment started with examining only used real image data for damage detection task with 43 training images and 19 validation images as the green dot shown in Fig. 4.''')

st.image("media/mAP.png", caption="Fig 4. mAP for damage detection with the increase of training set size.")

st.markdown('''The basic data augmentation method was performed on each image in training set. 
The damage detection models were trained on adding 2, 4, 6, 8, 10, 12, 14, 16, 18, 20 augmented images on original training set separately. 
The instance segmentation models were validated on the same validation set with 19 real images. 
The optimal quantity of basic augmented images is 8 and total number of training images is 387 which reached  85.8% mAP. 
The optimal quantity is determined where the model perform the highest mAP with the least quantity of training set. 
After figuring out the capability of basic data augmented images on improvement of damage detection system, 
the synthetic images started to evaluate. 
This process was designed since it is more time-consuming to generate synthetic images than basic augmentation methods. 
To balance the trade-off between time and model improvement, the synthetic images were added after basic augmentation evaluation. 
Similar to the process for adding basic augmentation images, the damage detection models were trained on adding 2, 4, 6, 8, 10 synthetic images on original training set and 8 basic augmented images separately. 
The optimal quantity of synthetic images is 6 and total number of training images is 645 which reached  88% mAP. 
The value of mAP in this experiment is shown in Table 1.''')

st.image("media/table-mAP.png", caption="mAP for different augmented images setting.")

st.markdown('''
### Limitations and Future Works
This study's findings are limited in their generalizability to similar turbine facilities. 
To improve the model's generalizability, future work should involve capturing real data from other hydropower 
turbine facilities of varying ages. The current synthetic image data set is based on only 43 images, 
which is a significant limitation. Additionally, incorporating diverse artificial lighting conditions using stable diffusion 
could better replicate various on-site settings. Presently, the damage detection system annotates all damages as a single class. 
Future research should focus on classifying different levels of damage severity and identifying specific types of damage, 
such as cavitation, frosting, pitting, and corrosion. Lastly, conducting a survey to gather domain experts' assessments of 
synthetic images could provide valuable insights. The survey would test their ability to distinguish between real and synthetic images, 
further validating the synthetic data's utility in training the model.

### Conclusions
This study marks a significant advancement in hydropower turbine blade inspection by integrating computer vision
with generative AI techniques. Utilizing Stable Diffusion with ControlNet reference-only methods, 
the research effectively overcomes the limitations of small real image datasets, enhancing the quality and 
diversity of training data. Analysis revealed that the synthetic data increased the mean Average Precision (mAP) 
by 6.3\%, primarily due to a more diverse damage area coverage ratio. The combination of traditional data
augmentation with synthetic data generation proved to be a robust approach, significantly improving the performance 
of the YOLOv8 instance segmentation model in damage detection. The findings highlight the potential of generative AI
to transcend the limitations of conventional inspection methods, leading to safer, more efficient, and more reliable 
turbine inspections. Future research could investigate the scalability of this method and its application to other
infrastructure assets, further broadening the impact of generative AI in industrial inspection tasks.''')


