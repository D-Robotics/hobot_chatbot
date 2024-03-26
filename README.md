English| [简体中文](./README_cn.md)

# Feature Introduction

**hobot_chatbot** Chatbot implements intelligent chat functionality on the client side without the need for an Internet connection. This application is based on intelligent voice, a large language model, and a text-to-speech module. It sends the intelligent voice ASR recognition results to the client-side large language model for processing, obtains the output results, and finally plays them back through the text-to-speech module.

# Bill of Materials

| Robot Name        | Manufacturer | Reference Link                                                |
| :-----------------| ------------ | ------------------------------------------------------------- |
| RDK X3 (4GB RAM)  | Multiple     | [Click here](https://developer.horizon.cc/rdkx3)              |
| Microphone Board  | Waveshare    | [Click here](https://www.waveshare.net/shop/Audio-Driver-HAT.htm) |

# Instructions for Use

## Preparation

Before starting the experience, you need to meet the following basic requirements:

- Confirm that the Horizon RDK is the 4GB RAM version
- The Horizon RDK has been flashed with the Horizon-provided Ubuntu 20.04 system image
- The audio board is correctly connected to the RDK X3, with headphones or speakers plugged into the headphone jack
- Install transformers with the command `pip3 install transformers -i https://pypi.tuna.tsinghua.edu.cn/simple`
- Update hobot-dnn with the command `sudo apt update; sudo apt install hobot-dnn`

## Robot Assembly

1. Connect the microphone board to the Horizon RDK X3 40PIN GPIO interface. The physical connection should appear as shown in the image below:

    ![x3pi_mic](./imgs/x3pi_mic.png)

2. Plug in headphones or speakers into the headphone jack.

## Install Package

After starting the RDK X3, connect to the robot via SSH or VNC in the terminal, copy and run the following command on the RDK system to complete the installation of the related Node.

```bash
sudo apt update
sudo apt install -y tros-hobot-chatbot
```

## Run Intelligent Chatbot

1. Before running the program, download the model files and unzip them.

    1. Download the large language model file

        ```bash
        # Download the large language model file
        wget http://sunrise.horizon.cc/llm-model/llm_model.tar.gz

        # Unzip
        sudo tar -xf llm_model.tar.gz -C /opt/tros/${TROS_DISTRO}/lib/hobot_llm/
        ```

   2. Download TTS model

       ```bash
       wget http://sunrise.horizon.cc//tts-model/tts_model.tar.gz
       sudo tar -xf tts_model.tar.gz -C /opt/tros/${TROS_DISTRO}/lib/hobot_tts/
       ```

2. Modify BPU reserved memory size and set CPU frequency

    Set BPU reserved memory size to 1.7GB, refer to [TODO]() for the method.

    After reboot, adjust CPU maximum frequency to 1.5GHz and set scheduling mode to `performance`, with the following commands:

    ```bash
    sudo bash -c 'echo 1 > /sys/devices/system/cpu/cpufreq/boost'
    sudo bash -c 'echo performance > /sys/devices/system/cpu/cpufreq/policy0/scaling_governor'
    ```

3. Configure intelligent speech module and load audio driver

   1. Copy configuration files

        ```shell
        # Copy the necessary configuration files for running examples from the installation path of tros.b, ignore if already copied
        cp -r /opt/tros/${TROS_DISTRO}/lib/hobot_audio/config/ .
        ```

   2. Modify *config/audio_config.json* and set the `asr_mode` field to `1`.

   3. Confirm the correct audio device settings, refer to the RDK user manual [Audio Interface Board](https://developer.horizon.cc/documents_rdk/hardware_development/rdk_x3/audio_board) for specific setup instructions.

   4. Configure tros.b environment and start the application

    ```shell
    # Configure tros.b environment
    source /opt/tros/setup.bash

    # Suppress debug print information
    export GLOG_minloglevel=3

    # Start the launch file
    ros2 launch hobot_chatbot chatbot.launch.py
    ```

    Once successfully launched, wake up the robot using the wake-up word "Horizon Hello" and start chatting with the robot. Note that each round of conversation must start by waking up the robot with the wake-up word "Horizon Hello".# Interface Description

## Topics

| Name         | Message Type                                                                                                            | Description                                    |
| ------------ | ----------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| /audio_smart | [audio_msg/msg/SmartAudioData](https://github.com/HorizonRDK/hobot_msgs/blob/develop/audio_msg/msg/SmartAudioData.msg) | Publishes intelligent results of smart audio processing |
| /audio_asr   | std_msgs/msg/String                                                                                                    | Publishes ASR recognition results               |
| /tts_text    | std_msgs/msg/String                                                                                                    | Publishes results of large language model       |

# Frequently Asked Questions

1. No response from the robot?

- Confirm if audio device connection is normal and headphones or speakers are connected
- Confirm if audio drivers are loaded
- Confirm if audio devices were connected before loading audio drivers
- Confirm that the `asr_mode` field in *config/audio_config.json* is set to `1`
- Confirm that the development board has 4GB of memory and modify the BPU reserved memory size to 1.7GB
