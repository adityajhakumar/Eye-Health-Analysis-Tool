

# Eye Health Analysis Tool

## Overview

The Eye Health Analysis Tool is a Streamlit application designed to analyze eye images and provide a health report based on predefined healthy eye parameters. It uses computer vision techniques to extract features from the eye images and compare them with established norms to generate a comprehensive report.

## Features

- **Image Upload**: Users can upload eye images for analysis.
- **Preprocessing**: The tool normalizes the image dimensions to ensure accurate analysis.
- **Feature Extraction**: Extracts key eye features such as pupil size and iris pattern.
- **Health Status**: Compares extracted features with healthy eye parameters to assess eye health.
- **Diopter Calculation**: Estimates the diopter value based on pupil size and corneal curvature.
- **Terms and Conditions**: Users must agree to the terms and conditions before accessing the analysis.

## Installation

To set up the Eye Health Analysis Tool locally, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/eye-health-analysis-tool.git
   cd eye-health-analysis-tool
   ```

2. **Create a Virtual Environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:

   Make sure you have `pip` installed, then run:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit App**:

   ```bash
   streamlit run app.py
   ```

   Open a web browser and navigate to `http://localhost:8501` to use the application.

## Usage

1. **Upload Image**: Click on the upload button to select and upload an eye image from your local filesystem.
2. **Input Details**: Enter the age and gender of the person whose eye image is uploaded.
3. **Agree to Terms**: You must agree to the terms and conditions before proceeding with the analysis.
4. **View Report**: The tool will display a detailed eye health report, including pupil size, iris pattern, health status, and diopter value.

## Terms and Conditions

Before using the tool, you must agree to the following terms:

- The Eye Health Analysis Tool provides an estimation of eye health based on predefined parameters and image analysis. It is intended for reference purposes only and should not be used as a substitute for professional medical advice or diagnosis.
- The accuracy of the analysis may vary depending on the quality of the image and other factors. The results provided are not guaranteed to be fully accurate.
- By using this tool, you acknowledge that the creators and operators of the Eye Health Analysis Tool are not responsible for any decisions made based on the information provided.

## Project Structure

- `app.py`: The main Streamlit application script.
- `requirements.txt`: Lists all the dependencies needed for the project.
- `assets/`: Directory for storing any additional files or images (optional).

## Contributing

Contributions to the Eye Health Analysis Tool are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please contact:

- **Email**: adityakumarjha292004@gmail.com
- **GitHub**: [your-username](https://github.com/adityajhakumar)

