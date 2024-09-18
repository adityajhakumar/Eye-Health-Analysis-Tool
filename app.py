import streamlit as st
import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import io

# Define healthy eye parameters
healthy_eye_params = {
    "age_groups": {
        "0-5": {
            "corneal_curvature_mm": 7.8,
            "pupil_size_mm": {"bright_light": 3.5, "dim_light": 7.5},
            "lens_clarity": "clear",
            "cup_to_disc_ratio": 0.3,
            "retinal_thickness_um": 270,
            "iris_pattern": "uniform"
        },
        "6-12": {
            "corneal_curvature_mm": 7.7,
            "pupil_size_mm": {"bright_light": 3.5, "dim_light": 7.5},
            "lens_clarity": "clear",
            "cup_to_disc_ratio": 0.3,
            "retinal_thickness_um": 275,
            "iris_pattern": "uniform"
        },
        "13-20": {
            "corneal_curvature_mm": 7.8,
            "pupil_size_mm": {"bright_light": 3.0, "dim_light": 7.0},
            "lens_clarity": "clear",
            "cup_to_disc_ratio": 0.3,
            "retinal_thickness_um": 280,
            "iris_pattern": "uniform"
        },
        "21-30": {
            "corneal_curvature_mm": 7.8,
            "pupil_size_mm": {"bright_light": 3.0, "dim_light": 7.0},
            "lens_clarity": "clear",
            "cup_to_disc_ratio": 0.3,
            "retinal_thickness_um": 285,
            "iris_pattern": "uniform"
        },
        "31-40": {
            "corneal_curvature_mm": 7.9,
            "pupil_size_mm": {"bright_light": 3.2, "dim_light": 6.8},
            "lens_clarity": "clear",
            "cup_to_disc_ratio": 0.35,
            "retinal_thickness_um": 290,
            "iris_pattern": "uniform"
        },
        "41-50": {
            "corneal_curvature_mm": 7.9,
            "pupil_size_mm": {"bright_light": 3.2, "dim_light": 6.5},
            "lens_clarity": "clear",
            "cup_to_disc_ratio": 0.35,
            "retinal_thickness_um": 295,
            "iris_pattern": "uniform"
        },
        "51-60": {
            "corneal_curvature_mm": 8.0,
            "pupil_size_mm": {"bright_light": 3.5, "dim_light": 6.2},
            "lens_clarity": "cloudy",
            "cup_to_disc_ratio": 0.4,
            "retinal_thickness_um": 300,
            "iris_pattern": "uniform"
        },
        "61-70": {
            "corneal_curvature_mm": 8.0,
            "pupil_size_mm": {"bright_light": 3.5, "dim_light": 6.0},
            "lens_clarity": "cloudy",
            "cup_to_disc_ratio": 0.4,
            "retinal_thickness_um": 305,
            "iris_pattern": "uniform"
        },
        "71-80": {
            "corneal_curvature_mm": 8.1,
            "pupil_size_mm": {"bright_light": 3.7, "dim_light": 6.0},
            "lens_clarity": "cloudy",
            "cup_to_disc_ratio": 0.45,
            "retinal_thickness_um": 310,
            "iris_pattern": "uniform"
        }
    },
    "gender": {
        "male": {
            "pupil_size_mm_adjustment": 0.2
        },
        "female": {
            "pupil_size_mm_adjustment": 0.15
        }
    }
}

# Load and preprocess image
def load_image(image_file):
    image = Image.open(image_file)
    image = np.array(image)
    return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

# Normalize image dimensions
def normalize_image(image, target_size=(500, 500)):
    return cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)

# Display image
def display_image(image, title="Image"):
    st.image(image, channels="BGR", caption=title)

# Extract features from image
def extract_features(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Pupil detection (simplified)
    _, thresholded = cv2.threshold(gray_image, 50, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    pupil_size_mm = None
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(largest_contour)
        # Convert radius from pixels to mm
        pupil_size_mm = radius * 2  # Diameter in pixels
    
    # Iris pattern (basic uniformity check)
    iris_pattern = "uniform"  # Placeholder

    return {
        "pupil_size_mm": pupil_size_mm,
        "iris_pattern": iris_pattern
    }

# Compare with healthy parameters
def compare_with_healthy(params, extracted_features, age, gender):
    # Determine the age group
    age_group = None
    if 0 <= age <= 5:
        age_group = "0-5"
    elif 6 <= age <= 12:
        age_group = "6-12"
    elif 13 <= age <= 20:
        age_group = "13-20"
    elif 21 <= age <= 30:
        age_group = "21-30"
    elif 31 <= age <= 40:
        age_group = "31-40"
    elif 41 <= age <= 50:
        age_group = "41-50"
    elif 51 <= age <= 60:
        age_group = "51-60"
    elif 61 <= age <= 70:
        age_group = "61-70"
    elif 71 <= age <= 80:
        age_group = "71-80"
    
    if age_group:
        reference_params = params["age_groups"].get(age_group, {})
        pupil_size_ref = reference_params.get("pupil_size_mm", {"bright_light": 3, "dim_light": 7})
        pupil_size_adjustment = params["gender"].get(gender, {}).get("pupil_size_mm_adjustment", 0)
        pupil_size_ref["bright_light"] += pupil_size_adjustment
        
        extracted_pupil_size = extracted_features.get("pupil_size_mm", None)
        if extracted_pupil_size is not None:
            deviation = abs(extracted_pupil_size - pupil_size_ref["bright_light"])
            result = "Normal" if deviation < 1 else "Abnormal"
        else:
            result = "Pupil size not detected"
        
        # Additional parameters check
        status = {
            "Pupil Size Status": result,
            "Corneal Curvature Status": "Normal",  # Placeholder
            "Lens Clarity Status": "Normal",  # Placeholder
            "Cup-to-Disc Ratio Status": "Normal",  # Placeholder
            "Retinal Thickness Status": "Normal"  # Placeholder
        }
    else:
        result = "Age group not defined"
        status = {}

    return result, status

def calculate_diopter(corneal_curvature_mm, pupil_size_mm):
    if pupil_size_mm <= 0:
        return "Pupil size is not valid for diopter calculation"
    
    # Convert mm to meters for calculations
    corneal_curvature_m = corneal_curvature_mm / 1000
    pupil_size_m = pupil_size_mm / 1000
    
    # Adjust the factor based on realistic models
    # Focal length in meters (example adjustment factor, may need calibration)
    focal_length_m = corneal_curvature_m / (pupil_size_m * 0.02)  # Example factor adjustment
    
    # Calculate diopter
    try:
        diopter = 1 / focal_length_m
    except ZeroDivisionError:
        return "Focal length cannot be zero"
    
    # Adjust diopter to a more realistic range if needed
    diopter = round(diopter, 2)
    if diopter > 30:
        diopter = 30  # Cap the diopter to a reasonable maximum value
    
    return diopter

# Generate report
def generate_report(extracted_features, comparison_result, status, corneal_curvature_mm):
    pupil_size_mm = extracted_features.get("pupil_size_mm", "Not detected")
    
    if isinstance(pupil_size_mm, (int, float)) and pupil_size_mm > 0:
        diopter = calculate_diopter(corneal_curvature_mm, pupil_size_mm)
    else:
        diopter = "Invalid pupil size for diopter calculation"

    report = {
        "Pupil Size (mm)": pupil_size_mm,
        "Iris Pattern": extracted_features.get("iris_pattern", "Not detected"),
        "Health Status": comparison_result,
        "Pupil Size Status": status.get("Pupil Size Status", "Unknown"),
        "Corneal Curvature Status": status.get("Corneal Curvature Status", "Unknown"),
        "Lens Clarity Status": status.get("Lens Clarity Status", "Unknown"),
        "Cup-to-Disc Ratio Status": status.get("Cup-to-Disc Ratio Status", "Unknown"),
        "Retinal Thickness Status": status.get("Retinal Thickness Status", "Unknown"),
        "Diopter": diopter
    }
    
    return report

# Streamlit app
def main():
    st.title("Eye Health Analysis Tool")

    st.write("## Terms and Conditions")
    st.write("""
    By using this Eye Health Analysis Tool, you agree to the following terms and conditions:
    
    1. **Accuracy of Results**: The results provided by this tool are for reference purposes only. The calculated values may not fully reflect your actual eye health or vision status.
    2. **No Professional Advice**: This tool does not replace professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified health provider with any questions you may have regarding a medical condition.
    3. **Limitation of Liability**: The developers of this tool are not liable for any inaccuracies or issues arising from the use of the provided information.
    4. **Data Privacy**: Your input data will not be stored or shared. The tool operates in your local environment and does not collect any personal data.
    
    By proceeding, you acknowledge that you have read, understood, and agree to these terms and conditions.
    """)
    
    agree = st.checkbox("I agree to the terms and conditions")

    if agree:
        uploaded_file = st.file_uploader("Upload the eye image:", type=["jpg", "jpeg", "png"])
        age = st.number_input("Enter the age of the person:", min_value=0, max_value=120, value=25)
        gender = st.selectbox("Enter the gender of the person:", ["male", "female"])

        if st.button("Analyze"):
            if uploaded_file:
                try:
                    # Load and preprocess image
                    image = load_image(uploaded_file)
                    normalized_image = normalize_image(image)
                    
                    # Display image
                    display_image(normalized_image, title="Normalized Eye Image")
                    
                    # Extract features
                    extracted_features = extract_features(normalized_image)
                    
                    # Compare with healthy parameters
                    comparison_result, status = compare_with_healthy(healthy_eye_params, extracted_features, age, gender)
                    
                    # Determine age group for report
                    age_group = None
                    if 0 <= age <= 5:
                        age_group = "0-5"
                    elif 6 <= age <= 12:
                        age_group = "6-12"
                    elif 13 <= age <= 20:
                        age_group = "13-20"
                    elif 21 <= age <= 30:
                        age_group = "21-30"
                    elif 31 <= age <= 40:
                        age_group = "31-40"
                    elif 41 <= age <= 50:
                        age_group = "41-50"
                    elif 51 <= age <= 60:
                        age_group = "51-60"
                    elif 61 <= age <= 70:
                        age_group = "61-70"
                    elif 71 <= age <= 80:
                        age_group = "71-80"
                    
                    corneal_curvature_mm = healthy_eye_params["age_groups"].get(age_group, {}).get("corneal_curvature_mm", 7.8)  # Default value if age group not found
                    report = generate_report(extracted_features, comparison_result, status, corneal_curvature_mm)
                    
                    st.write("## Eye Health Report:")
                    for key, value in report.items():
                        st.write(f"{key}: {value}")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please upload an image file.")
    else:
        st.info("Please agree to the terms and conditions to proceed.")

if __name__ == "__main__":
    main()
