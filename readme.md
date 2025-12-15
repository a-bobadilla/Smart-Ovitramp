# Automated and Continuous Ovitrap Monitoring System

This repository contains the necessary resources for implementing an IoT-based computer vision system for detecting mosquito larvae in smart ovitraps. The system utilizes an Edge Computing architecture with processing on a Jetson Nano and image capture via ESP32-CAM.

## About

Base files for the final degree project to obtain the title of Electronic Engineer with emphasis in Mechatronics from [FPUNA](https://www.pol.una.py/).

## Repository Structure

- **./3D Print/**: STL files for additive manufacturing of the structure.
- **./EasyEDA/**: Design files for the power and control PCB.
- **./dataset/**: Labelled images for neural network training.
- **smartovitbot.py**: Main script for data management and storage on the Jetson Nano.

---

## 1. Mechanical Manufacturing (Hardware)

The files for printing the physical structure are located in the `./3D Print/` folder.

**Printing Instructions:**
The design was validated using Fused Deposition Modeling (FDM). The following parameters are recommended to ensure the necessary robustness for outdoor environments:

- **Material:** PLA (Polylactic Acid).
- **Infill:** 20%.
- **Perimeters:** 3 layers.
- **Layer Height:** 0.2 mm.

**Post-processing:**
It is recommended to subject the resulting parts to a puttying and painting process to protect the device from the weather and increase its durability.

**Assembly:**
The structure includes a top support to house the ESP32-CAM board and the power board, as well as a protective roof against dust and debris. Ensure the LED lighting system has an inclination angle of 70° relative to the water to optimize larvae visualization.

---

## 2. Electronics and Power

The power management and lighting control system files are located in `./EasyEDA/`.

**Main Components:**

- **Development Board:** ESP32-CAM (OV2640 Camera).
- **Charge Management:** Module based on TP4056 for 18650 Lithium battery.
- **Battery:** Type 18650 (approx. 3000 mAh).
- **Lighting:** LEDs controlled by an S8050 transistor.
- **Connectivity:** TP-Link TL-MR3040 portable router (or compatible 4G USB modem).

**Board Functionality:**
The custom PCB allows selection between USB or external power (+12V DC). It includes a charge control circuit that supplies constant current until the battery reaches 4.2V. The lighting system is activated via a switching transistor controlled by the ESP32-CAM before each capture.

---

## 3. Model Training (AI)

The base data is found in `./dataset/`.

**Dataset Details:**

- The dataset contains captured and validated images (pH 6, controlled conditions).
- Images were labelled using **Roboflow**.
- Total original samples: 188 images (distributed into training, validation, and testing).

**Model:**
The **YOLOv5s** architecture is used due to its efficiency on low-power devices. If you wish to retrain the model:

1. Use the files in `./dataset/`.
2. Run the training (recommended in a GPU environment like Google Colab) for approximately 300 epochs.
3. Export the model weights for implementation on the Jetson Nano.

---

## 4. Implementation and Software (Jetson Nano)

The central processing unit is an **NVIDIA Jetson Nano**.

**Prerequisites:**

- Install **Node-RED** on the Jetson Nano:
  ```bash
  bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)
  ```
- Configure an MQTT Broker (e.g., Mosquitto):
  ```bash
  sudo apt update
  sudo apt install mosquitto mosquitto-clients
  ```
- Install necessary Python libraries:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

**Step-by-Step Deployment:**

1. **Communication Configuration:**
   The ESP32-CAM must be configured to send images via MQTT protocol to the Broker hosted on the Jetson Nano or the local network created by the TL-MR3040.

2. **Management Script Execution:**
   Run the script for data storage and management:

   ```bash
   python3 smartovitbot.py
   ```

   _This script handles the data flow coming from the ovitraps._

3. **Processing Flow (Node-RED):**
   Import the Node-RED workflow that performs the following tasks:
   - **MQTT Subscription:** Receives the image in Base64.
   - **Preprocessing:** Decodes the Base64 string to an image.
   - **Inference (Tensor.js):** Executes the trained YOLOv5 model on the image.
   - **Filtering:** Checks if the larvae detection count is > 0.
   - **Notification:** Sends the image and the number of detected larvae to a Telegram Bot.

## 5. Implementation Manual

For detailed instructions on system deployment and configuration, please refer to the official manual:

- 📖 [**Manual Ovitrampa.pptx**](./Manual%20Ovitrampa.pptx)

## Contact and Credits

Developed as part of the Electronics Engineering degree project - [FPUNA](https://www.pol.una.py/).
