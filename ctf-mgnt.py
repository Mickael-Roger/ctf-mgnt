#!/usr/bin/env python

import argparse
import os
import time
import platform

###
# Configuration
###

DataDir = "/home/mickael/CTFs/ctfs"
ImagesDir = "/home/mickael/CTFs/base-images"


####

def main():

  parser = argparse.ArgumentParser()
  
  parser.add_argument("-a", "--action", help = "Action", choices=['create', 'stop', 'start', 'delete', 'connect'], required=True)
  
  parser.add_argument("-C", "--ctf", help = "CTF Name", required=True)
  parser.add_argument("-c", "--chall", help = "Challenge Name", required=True)
  
  parser.add_argument("-b", "--base", help = "Base Image (Default Kali)", default="kali")

  args = parser.parse_args()


  match args.action:
    case "create":
        create(args.ctf, args.chall, args.base)

    case "delete":
        delete(args.ctf, args.chall)

    case "stop":
        stop(args.ctf, args.chall)

    case "start":
        start(args.ctf, args.chall)

    case "connect":
        connect(args.ctf, args.chall)



def createCtf(ctf):
    
    # Does not break if CTF already exist
    directory=os.path.join(DataDir, ctf)

    if not os.path.exists(directory):
      os.makedirs(directory)


def createChall(ctf, chall):
    # Break if Challenge already exist
    os.mkdir(os.path.join(DataDir, ctf, chall))
    os.mkdir(os.path.join(DataDir, ctf, chall, "vm"))
    os.mkdir(os.path.join(DataDir, ctf, chall, "data"))


def printIP(ctf, chall):
    os.system("virsh --connect qemu:///system domifaddr " + ctf + "-" + chall)


def connect(ctf, chall):
    print("TODO")

def createVm(ctf, chall, base):

    # Create VM Image from Base
    #os.system("qemu-img create -f qcow2 -b " + os.path.join(ImagesDir, base) + ".qcow2 -F qcow2 " + os.path.join(DataDir, ctf, chall, "vm", "vm.qcow2") + " 20G")
    os.system("cp " + os.path.join(ImagesDir, base) + ".qcow2 " + os.path.join(DataDir, ctf, chall, "vm", "vm.qcow2"))

    # Create the cloud init file
    os.system("genisoimage -output " + os.path.join(DataDir, ctf, chall, "vm", "cidata.iso") + " -V cidata -r -J " + os.path.join(ImagesDir, "user-data") + " " + os.path.join(ImagesDir, "meta-data")) 


    # Create the VMs
    if platform.freedesktop_os_release()['NAME'] == 'NixOS':
        extra_opt="--xml ./devices/filesystem/binary/@path=/run/current-system/sw/bin/virtiofsd" 
    else:
        extra_opt=""


    os.system("virt-install --connect qemu:///system --name=" + ctf + "-" + chall + " --ram=4096 --vcpus=2 --import --disk path=" + os.path.join(DataDir, ctf, chall, "vm", "vm.qcow2") + ",format=qcow2 --disk path=" + os.path.join(DataDir, ctf, chall, "vm", "cidata.iso") + ",device=cdrom --os-variant=debian12 --network default --graphics vnc,listen=0.0.0.0 --noautoconsole --xml ./memoryBacking/access/@mode=shared --xml ./memoryBacking/source/@type=memfd --xml ./devices/filesystem/@type=mount --xml ./devices/filesystem/@accessmode=passthrough --xml ./devices/filesystem/driver/@type=virtiofs --xml ./devices/filesystem/source/@dir=" + os.path.join(DataDir, ctf, chall, "data") + " --xml ./devices/filesystem/target/@dir=ctf_user --xml ./devices/filesystem/alias/@name=fs0 --xml ./devices/filesystem/address/@type=pci --xml ./devices/filesystem/address/@domain=0x0000 --xml ./devices/filesystem/address/@bus=0x07 --xml ./devices/filesystem/address/@slot=0x00 --xml ./devices/filesystem/address/@function=0x0 " + extra_opt)
    #os.system("virt-install --connect qemu:///system --name=" + ctf + "-" + chall + " --ram=4096 --vcpus=2 --import --disk path=" + os.path.join(DataDir, ctf, chall, "vm", "vm.qcow2") + ",format=qcow2 --os-variant=debian12 --network default --graphics vnc,listen=0.0.0.0 --noautoconsole")

    os.system("chmod 777 " + os.path.join(DataDir, ctf, chall, "data")) 

    time.sleep(30)

    stop(ctf, chall)
    time.sleep(10)
    start(ctf, chall)

    time.sleep(30)


def stop(ctf, chall):
    os.system("virsh --connect qemu:///system destroy " + ctf + "-" + chall)

def start(ctf, chall):
    os.system("virsh --connect qemu:///system start " + ctf + "-" + chall)
    printIP(ctf, chall)


def delete(ctf, chall):

    # Stop and destroyVM
    stop(ctf, chall)
    os.system("virsh --connect qemu:///system undefine " + ctf + "-" + chall)

    # Delete VM related files
    os.system("rm -rf " + os.path.join(DataDir, ctf, chall, "vm"))


def create(ctf, chall, base):
    
    createCtf(ctf);
    createChall(ctf, chall);

    createVm(ctf, chall, base)



if __name__ == "__main__":
    main()
