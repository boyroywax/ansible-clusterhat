# Clusterhat CPU Mining Mini-Cluster

## ClusterHat Resources
* [2018-10-13 Latest USBboot image for <= RPI3B+](http://dist.8086.net/clusterhat/ClusterHAT-2018-10-09-lite-1-usbboot.zip)
* [ClusterHat USBboot Setup](https://8086.support/content/23/88/en/guide-to-using-the-rpiboot-test-image-on-the-cluster-hat_zero-stem-or-just-a-usb-cable.html) and [another version](https://8086.support/content/23/85/en/how-do-i-setup-usbboot-no-sd-cards-in-the-pi-zeros-for-the-cluster-hat.html)
* [WriteUp on Clusterhat in Google Groups](https://groups.google.com/forum/#!topic/clusterhat/vwiVEcjz3L0)
* [ClusterHat software control](https://clusterhat.com/setup-control)
* [Clusterhat control tool code](https://github.com/burtyb/clusterhat-image/blob/master/files/sbin/clusterhat)

## Load SSH keys to Pi0's
This is done on the RPi Cluster Controller
```bash
ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa && \
mkdir -p /var/lib/clusterhat/nfs/p{1,2,3,4}/home/pi/.ssh/ && \
cat ~/.ssh/id_rsa.pub >> /var/lib/clusterhat/nfs/p1/home/pi/.ssh/authorized_keys && \
cat ~/.ssh/id_rsa.pub >> /var/lib/clusterhat/nfs/p2/home/pi/.ssh/authorized_keys && \
cat ~/.ssh/id_rsa.pub >> /var/lib/clusterhat/nfs/p3/home/pi/.ssh/authorized_keys && \
cat ~/.ssh/id_rsa.pub >> /var/lib/clusterhat/nfs/p4/home/pi/.ssh/authorized_keys
```

## Start zero cluster
```bash
clusterhat on && \
sudo rpiboot -d /var/lib/clusterhat/boot/ -o -l -v
```

## Ansible Update cluster

- Create local SSH keys
- SSH copy local keys to controller and PiZs
- Update and Upgrade all hosts
- Clean up apt
- 

## Creating Backup images
https://medium.com/@mabrams_46032/kubernetes-on-raspberry-pi-c246c72f362f

Find the End of the drive
```bash
sudo fdisk -l /dev/$SD_DRIVE
```
ON MAC-OSX
```bash
diskutil list
```

Copy the Image up to the END
```bash
sudo dd if=$SD_DRIVE of=/Users/jdev/Documents/sd_backup.img bs=512 count=124928
```

## Ansible install Docker on all devices
[Pizero's need docker.service edited for Docker to run](https://dietpi.com/phpbb/viewtopic.php?t=5227&start=10)

pizero
sudo apt install docker.io --fix-missing

still need to get swarm working

## Docker on Raspberry Pi Zero W

```bash
docker service create --name miner \
    
```

## Mining on raspberry pi docker
https://github.com/alexellis/mine-with-docker

```bash
docker service create --name miner \
    boyroywax/cpuminer-multi:20190511-armhf cpuminer \
    --url=stratum+tcp://us-east.stratum.slushpool.com:3333 \
    --algo=sha256d \
    --userpass=<user>:<pass>
```
```bash
docker swarm init
```

```bash
docker swarm join --token <token> <swarm_master_ip>:2377
```

### Raspberry Pi Spec Comparison

RPI-3B+ Specs:
* Broadcom BCM2837B0, Cortex-A53 (ARMv8) 64-bit SoC @ 1.4GHz
* 1GB LPDDR2 SDRAM
* 2.4GHz and 5GHz IEEE 802.11.b/g/n/ac wireless LAN, Bluetooth 4.2, BLE
* Gigabit Ethernet over USB 2.0 (maximum throughput 300 Mbps)
* Extended 40-pin GPIO header
* Full-size HDMI
* 4 USB 2.0 ports
* CSI camera port for connecting a Raspberry Pi camera
* DSI display port for connecting a Raspberry Pi touchscreen display
* 4-pole stereo output and composite video port
* Micro SD port for loading your operating system and storing data
* 5V/2.5A DC power input
* Power-over-Ethernet (PoE) support (requires separate PoE HAT)

RPI-ZERO-W Specs:
* ARMv6 single core proc
* Broadcom BCM2835.  This contains an ARM1176JZFS (ARM11 using an ARMv6-architecture core) with floating point, running at 1GHz, and a Videocore 4 GPU.

### Building for RPI-3B+
```bash
sudo apt-get install -y automake autoconf pkg-config libopenssl-devel libcurl4-openssl-dev libjansson-dev libssl-dev libgmp-dev make g++ git
```

```bash
git clone https://github.com/tpruvot/cpuminer-multi.git
```

```bash
sudo ./autogen.sh && \
sudo ./configure --disable-assembly CFLAGS="-march=native -mfpu=neon" --with-crypto --with-curl && \
sudo make install
```

```bash
sudo cpuminer --url="stratum+tcp://us-east.stratum.slushpool.com:3333" \
--algo=sha256d \
--userpass="<username>.<worker>:<password>"
```

### Building for RPI Zero W
```bash
sudo apt-get install -y automake autoconf pkg-config libcurl4-openssl-dev libjansson-dev libssl-dev openssl libgmp-dev make g++ git
```

```bash
git clone https://github.com/tpruvot/cpuminer-multi.git
```

```bash
sudo ./autogen.sh && \
sudo ./configure --disable-assembly CFLAGS="-march=native" --with-crypto --with-curl && \
sudo make install
```

```bash
docker service create --name miner \
    boyroywax/cpuminer-multi-armv6:latest cpuminer \
    -a cryptonight \
    -o stratum+tcp://cryptonight.usa.nicehash.com:3355 \
    -u <user_name>
```

