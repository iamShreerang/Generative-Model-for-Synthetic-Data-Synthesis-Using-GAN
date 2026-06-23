import streamlit as st
import requests
import os
from PIL import Image
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Synthetic Data Generation Platform", layout="wide", page_icon="🧬")

# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Home", "Dataset Manager", "Training", "Generate", "Evaluation"],
        icons=["house", "database", "play-circle", "image", "bar-chart"],
        default_index=0,
    )
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("**Synthetic Data Generation Platform**")
    st.markdown("Using Deep Convolutional GAN")

# API Base URL
API_URL = "http://localhost:8888"

if selected == "Home":
    st.title("🧬 Synthetic Data Generation Platform")
    st.markdown("### Generate Realistic Synthetic Medical Images Using Deep Learning")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model", "DCGAN")
    with col2:
        st.metric("Status", "Ready")
    with col3:
        st.metric("Generated Images", "0")
    
    st.markdown("---")
    st.markdown("### Features")
    st.markdown("✅ Upload custom datasets")
    st.markdown("✅ Train DCGAN models")
    st.markdown("✅ Generate synthetic images")
    st.markdown("✅ Evaluate with FID, SSIM, PSNR")
    
    st.markdown("---")
    st.markdown("### Quick Start")
    st.markdown("1. Upload your dataset in **Dataset Manager**")
    st.markdown("2. Configure and start training in **Training**")
    st.markdown("3. Generate synthetic images in **Generate**")
    st.markdown("4. Evaluate results in **Evaluation**")

elif selected == "Dataset Manager":
    st.title("📁 Dataset Manager")
    
    tab1, tab2 = st.tabs(["Upload Dataset", "View Datasets"])
    
    with tab1:
        st.subheader("Upload New Dataset")
        dataset_name = st.text_input("Dataset Name", "my_dataset")
        uploaded_files = st.file_uploader("Upload Images", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
        
        if st.button("Upload"):
            if uploaded_files:
                with st.spinner("Uploading..."):
                    try:
                        files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
                        response = requests.post(f"{API_URL}/upload-dataset/?dataset_name={dataset_name}", files=files)
                        if response.status_code == 200:
                            st.success(f"✅ {response.json()['message']}")
                        else:
                            st.error(f"Upload failed: {response.text}")
                    except Exception as e:
                        st.error(f"Upload error: {str(e)}")
            else:
                st.warning("Please select files to upload")
    
    with tab2:
        st.subheader("Available Datasets")
        try:
            response = requests.get(f"{API_URL}/datasets/")
            if response.status_code == 200:
                datasets = response.json()['datasets']
                if datasets:
                    for ds in datasets:
                        col1, col2, col3 = st.columns([2, 1, 1])
                        col1.write(f"**{ds['name']}**")
                        col2.write(f"Images: {ds['image_count']}")
                        col3.write(f"📂 {ds['path']}")
                else:
                    st.info("No datasets available")
        except:
            st.error("Cannot connect to API. Make sure the backend is running.")

elif selected == "Training":
    st.title("🎯 Model Training")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Training Configuration")
        
        dataset_name = st.text_input("Dataset Name", "glioma")
        epochs = st.slider("Epochs", 10, 200, 50)
        batch_size = st.selectbox("Batch Size", [16, 32, 64], index=1)
        learning_rate = st.number_input("Learning Rate", value=0.0002, format="%.4f")
        image_size = st.selectbox("Image Size", [64, 128, 256], index=1)
        
        if st.button("🚀 Start Training", type="primary"):
            config = {
                "dataset_name": dataset_name,
                "epochs": epochs,
                "batch_size": batch_size,
                "learning_rate": learning_rate,
                "image_size": image_size
            }
            try:
                response = requests.post(f"{API_URL}/train/", json=config)
                if response.status_code == 200:
                    st.success("Training started!")
                else:
                    st.error(response.json().get('detail', 'Training failed'))
            except:
                st.error("Cannot connect to API")
    
    with col2:
        st.subheader("Training Status")
        
        if st.button("🔄 Refresh Status"):
            try:
                response = requests.get(f"{API_URL}/training-status/")
                if response.status_code == 200:
                    status = response.json()
                    
                    st.markdown(f"""
                    **Is Training:** {status['is_training']}  
                    **Current Epoch:** {status['current_epoch']}/{status['total_epochs']}  
                    **Generator Loss:** {status['gen_loss']:.4f}  
                    **Discriminator Loss:** {status['disc_loss']:.4f}
                    """)
                    
                    if status['is_training'] and status['total_epochs'] > 0:
                        progress = status['current_epoch'] / status['total_epochs']
                        st.progress(progress)
            except:
                st.error("Cannot fetch status")

elif selected == "Generate":
    st.title("🎨 Generate Synthetic Images")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Generation Settings")
        
        num_samples = st.slider("Number of Images", 1, 100, 16)
        
        try:
            response = requests.get(f"{API_URL}/models/")
            if response.status_code == 200:
                models = response.json()['models']
                if models:
                    model_names = [m['name'] for m in models]
                    selected_model = st.selectbox("Select Model", model_names)
                    model_path = next((m['path'] for m in models if m['name'] == selected_model), None)
                else:
                    st.warning("No trained models available")
                    model_path = None
        except:
            st.error("Cannot load models")
            model_path = None
        
        if st.button("✨ Generate Images", type="primary"):
            if model_path:
                with st.spinner("Generating..."):
                    try:
                        response = requests.post(f"{API_URL}/generate/", json={"num_samples": num_samples, "model_path": model_path})
                        if response.status_code == 200:
                            result = response.json()
                            st.success(f"✅ {result['message']}")
                            st.info(f"Saved to: {result['output_dir']}")
                            st.session_state['output_dir'] = result['output_dir']
                            st.rerun()
                        else:
                            st.error(f"Generation failed: {response.text}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.error("Please train a model first")
    
    with col2:
        st.subheader("Generated Samples")
        
        # Try to find latest generated folder
        synth_data_path = "./Synthetic Data"
        if os.path.exists(synth_data_path):
            folders = [f for f in os.listdir(synth_data_path) if os.path.isdir(os.path.join(synth_data_path, f))]
            if folders:
                latest_folder = sorted(folders)[-1]
                output_dir = os.path.join(synth_data_path, latest_folder)
                
                if 'output_dir' in st.session_state:
                    output_dir = st.session_state['output_dir']
                
                if os.path.exists(output_dir):
                    image_files = sorted([f for f in os.listdir(output_dir) if f.endswith('.png') and 'grid' not in f])
                    if image_files:
                        st.write(f"Showing {len(image_files)} images from: {os.path.basename(output_dir)}")
                        cols = st.columns(4)
                        for idx, img_file in enumerate(image_files[:16]):
                            with cols[idx % 4]:
                                img_path = os.path.join(output_dir, img_file)
                                img = Image.open(img_path)
                                st.image(img, use_container_width=True)
                    else:
                        st.info("No images in folder")
                else:
                    st.info("Generate images to see them here")
            else:
                st.info("No generated folders found")
        else:
            st.info("Generate images to see them here")

elif selected == "Evaluation":
    st.title("📊 Model Evaluation")
    
    st.subheader("Evaluation Metrics")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Calculate Metrics")
        
        real_dataset = st.selectbox("Real Dataset", ["glioma", "meningioma", "notumor", "pituitary"])
        
        if 'output_dir' in st.session_state:
            synthetic_dir = st.session_state['output_dir']
        else:
            synthetic_dir = st.text_input("Synthetic Images Folder", "./Synthetic Data/generated_from_trained")
        
        if st.button("Calculate Metrics"):
            if os.path.exists(synthetic_dir):
                with st.spinner("Calculating metrics..."):
                    try:
                        from src.data.preprocessor import DataPreprocessor
                        from src.evaluation.metrics import Evaluator
                        
                        preprocessor = DataPreprocessor(image_size=128)
                        real_images = preprocessor.load_dataset(f"./Dataset/{real_dataset}")[:16]
                        
                        synth_images = []
                        for f in os.listdir(synthetic_dir):
                            if f.endswith('.png') and 'grid' not in f:
                                img = Image.open(os.path.join(synthetic_dir, f))
                                synth_images.append(np.array(img) / 255.0)
                        
                        synth_images = np.array(synth_images[:16])
                        
                        import numpy as np
                        metrics = Evaluator.evaluate_all(real_images, synth_images)
                        
                        st.session_state['metrics'] = metrics
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Evaluation error: {str(e)}")
            else:
                st.error("Synthetic images directory not found")
    
    with col2:
        st.markdown("### Results")
        
        if 'metrics' in st.session_state:
            metrics = st.session_state['metrics']
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("FID Score", f"{metrics['fid']:.2f}", help="Lower is better")
            with col_b:
                st.metric("SSIM", f"{metrics['ssim']:.4f}", help="0-1, Higher is better")
            with col_c:
                st.metric("PSNR", f"{metrics['psnr']:.2f}", help="Higher is better")
        else:
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("FID Score", "N/A", help="Calculate to see")
            with col_b:
                st.metric("SSIM", "N/A", help="Calculate to see")
            with col_c:
                st.metric("PSNR", "N/A", help="Calculate to see")

st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ using Streamlit & TensorFlow")
