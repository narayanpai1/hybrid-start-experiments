# Instructions to build a custom kernel


1. ### **Add the source for Linux source-code to sources.list**

    This is done by uncommenting the desired deb-src lines.

    For eg, in Ubuntu the following line

    ```
    deb-src http://in.archive.ubuntu.com/ubuntu focal main restricted
    ```

2. ### **Download the source code of the current kernel**

    ```bash
    $ sudo apt-get source linux-image-unsigned-$(uname -r)
    ```

3. ### **Install Required Packages**

    Install additional packages required for building a kernel. 

    ```bash
    $ sudo apt-get install git fakeroot build-essential ncurses-dev xz-utils libssl-dev bc flex libelf-dev bison
    ```

4. ### **Perform required changes**

    For this experiment, perform the required changes in `net/ipv4/tcp_cubic.c`.

5. ### **Configure Kernel Parameters**

    The Linux kernel source code comes with the default configuration. However, you can apply the configuration of your current kernel to the downloaded kernel as follows:

    ```bash
    $ cd linux-5.9.6
    $ cp -v /boot/config-$(uname -r) .config
    $ make menuconfig
    ```

6. ### **Build the Kernel**

    6.1 Start building the kernel by running the following command:

      ```bash
      $ sudo make
      ```
    
    6.2 Install the required modules with this command:

      ```bash
      $ sudo make modules_install
      ```
      
    6.3 Install the kernel by:

      ```bash
      $ sudo make install 
      ```

7. ### **Reboot**

    ```bash
    $ sudo reboot
    ```

8. ### **Verify Kernel Version**

    ```bash
    uname -mrs
    ```
