#!/bin/bash
export password='test'
vlc -I telnet --telnet-password $password
