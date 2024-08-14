# Configure a Paperspace Server

We'll use the Paperspace Console, not their API, to configure a server.  
Paperspace must be contacted in advance to approve your account for a given 
server configuration.

The following notes start by following the Paperspace [documentation]
(https://docs.digitalocean.com/products/paperspace/machines/getting-started
/quickstart/) using [Run ML in a Box](https://docs.digitalocean.
com/products/paperspace/machines/getting-started/run-ml-in-a-box/) to set up the basic machine and install the Nvidia drivers.

1. Visit the [Paperspace Console](https://console.paperspace.com/)
2. Switch from "Gradient" to "Core".
3. Choose Public IPs and claim a static IP address.
2. Select "Create a Machine".
3. Enter payment information.
4. Select "Multi-GPU" and choose A5000x2, or whichever GPUs are needed.
5. Wait for approval email.
6. Create machine and choose an OS template with ML-in-a-Box.  That will 
   make sure the Nvidia drivers are installed.
7. Wait for machine to start up
8. Use the Public IPs tab to assign a static IP address.

Once up and running you can access the machine via ssh to the static IP address.

Follow the [Run in a Box](https://docs.digitalocean.com/products/paperspace/machines/getting-started/run-ml-in-a-box/) instructions.

Running this command describes the server/gpu configuration:

```python -m torch.utils.collect_env```

The output looks like this:

```
paperspace@...:~$ python -m torch.utils.collect_env
Collecting environment information...
PyTorch version: 1.12.1+cu116
Is debug build: False
CUDA used to build PyTorch: 11.6
ROCM used to build PyTorch: N/A

OS: Ubuntu 20.04.6 LTS (x86_64)
GCC version: (Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0
Clang version: Could not collect
CMake version: version 3.25.20230112-ge4c281e
Libc version: glibc-2.31

Python version: 3.9.16 (main, Dec  7 2022, 01:11:51)  [GCC 9.4.0] (64-bit runtime)
Python platform: Linux-5.4.0-147-generic-x86_64-with-glibc2.31
Is CUDA available: True
CUDA runtime version: 11.7.99
GPU models and configuration: 
GPU 0: NVIDIA RTX A5000
GPU 1: NVIDIA RTX A5000

Nvidia driver version: 515.105.01
cuDNN version: Probably one of the following:
/usr/lib/x86_64-linux-gnu/libcudnn.so.8.5.0
/usr/lib/x86_64-linux-gnu/libcudnn_adv_infer.so.8.5.0
/usr/lib/x86_64-linux-gnu/libcudnn_adv_train.so.8.5.0
/usr/lib/x86_64-linux-gnu/libcudnn_cnn_infer.so.8.5.0
/usr/lib/x86_64-linux-gnu/libcudnn_cnn_train.so.8.5.0
/usr/lib/x86_64-linux-gnu/libcudnn_ops_infer.so.8.5.0
/usr/lib/x86_64-linux-gnu/libcudnn_ops_train.so.8.5.0
HIP runtime version: N/A
MIOpen runtime version: N/A
Is XNNPACK available: True

Versions of relevant libraries:
[pip3] numpy==1.23.2
[pip3] torch==1.12.1+cu116
[pip3] torchaudio==0.12.1+cu116
[pip3] torchvision==0.13.1+cu116
[conda] Could not collect
paperspace@...:~$ 
```

The two A5000 GPUs are listed.


Forward the domain name to the server.

Now set up djangollmapi using the [HOWTO](HOWTO.md) in this repo.


