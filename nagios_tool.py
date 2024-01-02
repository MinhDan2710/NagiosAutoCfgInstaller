import os
import subprocess
import re
import string
import paramiko
import getpass
from tqdm import tqdm
import time
from paramiko.ssh_exception import SSHException
from colorama import Fore, Style
import signal
import sys


def main():
    signal.signal(signal.SIGINT, sigint_handler)
    os.system('clear')
    while True:
        menu()

        choice = input("Select a server or enter 0 to exit: ")
        # filepath = '/usr/local/nagios/etc/nagios.cfg' mac dinh
        # bỏ comment ở dưới dòng choice để mở hàm uncomment_cfg_dir
        filepath = '/usr/local/nagios/etc/nagios.cfg'

        if choice == "0":
            break

        if choice == "1":
            chmod_command = "sudo chmod 777 /usr/local/nagios/etc/nagios.cfg"
            subprocess.run(chmod_command, shell=True, check=True)

            # Gọi hàm uncomment_cfg_dir_ubuntu_windows
            edit_config_file.uncomment_cfg_dir_ubuntu_windows('/usr/local/nagios/etc/nagios.cfg')
            # uncomment_cfg_dir_ubuntu_windows(filepath)

            # Xử lý máy chủ Ubuntu
            host_name, alias, contact_group, ip_address, file_name = input_info.input_server_info_linux()

            # gọi hàm
            create_host_config.create_host_config_ubuntu(host_name, alias, contact_group, ip_address, file_name)

        elif choice == "2":
            chmod_command = "sudo chmod 777 /usr/local/nagios/etc/nagios.cfg"
            subprocess.run(chmod_command, shell=True, check=True)

            # Gọi hàm uncomment_cfg_dir_ubuntu_windows
            edit_config_file.uncomment_cfg_dir_ubuntu_windows('/usr/local/nagios/etc/nagios.cfg')
            # uncomment_cfg_dir_ubuntu_windows(filepath)

            # Xử lý máy chủ Windows
            host_name, alias, contact_group, ip_address, file_name = input_info.input_server_info_windows()
            # gọi hàm
            create_host_config.create_host_config_windows(host_name, alias, contact_group, ip_address, file_name)

        elif choice == "3":
            chmod_command = "sudo chmod 777 /usr/local/nagios/etc/nagios.cfg"
            subprocess.run(chmod_command, shell=True, check=True)

            # Gọi hàm uncomment_cfg_dir_ubuntu_windows
            edit_config_file.uncomment_cfg_dir_ubuntu_windows('/usr/local/nagios/etc/nagios.cfg')
            # uncomment_cfg_dir_routers(filepath)

            # Xử lý máy chủ Router
            host_name, alias, contact_group, ip_address, file_name, oid_port_in, oid_port_out = input_info.input_server_info_router()
            # gọi hàm
            create_host_config.create_host_config_router(host_name, alias, contact_group, ip_address, file_name, oid_port_in, oid_port_out)

        elif choice == "4":
            chmod_command = "sudo chmod 777 /usr/local/nagios/etc/nagios.cfg"
            subprocess.run(chmod_command, shell=True, check=True)

            # Gọi hàm uncomment_cfg_dir_ubuntu_windows
            edit_config_file.uncomment_cfg_dir_ubuntu_windows('/usr/local/nagios/etc/nagios.cfg')
            # uncomment_cfg_dir_ubuntu_windows(filepath)

            # Xử lý máy chủ Windows
            host_name, alias, contact_group, ip_address, file_name = input_info.input_server_info_windows()
            # gọi hàm
            create_host_config.create_host_config_windows_server(host_name, alias, contact_group, ip_address, file_name)


        else:
            print("-------------------------------------------")
            print("Invalid selection. Choose from 1 to 4.")
            print("-------------------------------------------")
    os.system('clear')


def sigint_handler(signum, frame):
    print(Fore.RED + "\nCtrl-C detected. Exiting..." + Style.RESET_ALL)
    sys.exit(0)

class create_host_config:
    @staticmethod
    def create_host_config_ubuntu(host_name, alias, contact_group, ip_address, file_name):
        host_config = f"""
        ################################################################################
        #                                                                              #
        #                              HOST DEFINITIONS                                #
        #                                                                              #
        ################################################################################

        # Here's the definition for "Host" notifications:
        # d = send notifications on a DOWN state,
        # u = send notifications on an UNREACHABLE state,
        # r = send notifications on recoveries (OK state),
        # f = send notifications when the host starts and stops flapping,
        # s = send notifications when scheduled downtime starts and ends.

    define host{{
            use                     	linux-server
            host_name               	{host_name}
            alias                   	{alias}
            address                 	{ip_address}
            check_period            	24x7
            check_command           	check-host-alive
            check_interval          	9
            retry_interval          	1
            max_check_attempts      	5
            notification_period     	24x7
            notification_options    	d,u,r,s
            notification_interval   	10
            contact_groups          	{contact_group}
    }}

    """

        ping_service_config = f"""
        ################################################################################
        #                                                                              #
        #                              SERVICE DEFINITIONS                             #
        #                                                                              #
        ################################################################################


        # Here's the definition for "Service" notifications:
        # w = send notifications on a WARNING state,
        # u = send notifications on an UNKNOWN state,
        # c = send notifications on a CRITICAL state,
        # r = send notifications on recoveries (OK state),
        # f = send notifications when the service starts and stops flapping,
        # s = send notifications when scheduled downtime starts and ends.

    define service{{
            use                             local-service
            host_name                       {host_name}
            service_description             PING
            check_command                   check_ping!100.0,20%!500.0,60%
            check_period            	    24x7
            check_interval          	    9
            retry_interval          	    1
            max_check_attempts      	    5
            notification_period             24x7
            notification_options            w,u,c,r,f
            notification_interval           10
            contact_groups                  {contact_group}
    }}

        """

        ssh_service_config = f"""
    define service{{

            use                             local-service
            host_name                       {host_name}
            service_description             SSH
            check_command                   check_ssh
            check_period            	    24x7
            check_interval          	    9
            retry_interval          	    1
            max_check_attempts      	    5
            notification_period             24x7
            notification_options            w,u,c,r,f
            notification_interval           10
            contact_groups                  {contact_group}
    }}

        """

        disk_usage_config = f"""
    define service{{

            use                             local-service
            host_name                       {host_name}
            service_description             Disk Usage - /tmp
            check_command                   check_nrpe!check_hda1!20!10!/
            check_period            	    24x7
            check_interval          	    9
            retry_interval          	    1
            max_check_attempts      	    5
            notification_period             24x7
            notification_options            w,u,c,r,f
            notification_interval           10
            contact_groups                  {contact_group}
    }}

        """
        ram_usage_config = f"""
    define service{{

            use                             local-service
            host_name                       {host_name}
            service_description             RAM Usage
            check_command                   check_nrpe!check_swap 
            check_period            	    24x7
            check_interval          	    9
            retry_interval          	    1
            max_check_attempts      	    5
            notification_period             24x7
            notification_options            w,u,c,r,f
            notification_interval           10
            contact_groups                  {contact_group}
        }}

        """
        current_load_config = f"""
    define service{{

            use                             local-service
            host_name                       {host_name}
            service_description             Current Load
            check_command                   check_nrpe!check_load
            check_period            	    24x7
            check_interval          	    9
            retry_interval          	    1
            max_check_attempts      	    5
            notification_period             24x7
            notification_options            w,u,c,r,f
            notification_interval           10
            contact_groups                  {contact_group}
    }}

        """
        current_user_config = f"""
    define service{{

            use                             local-service
            host_name                       {host_name}
            service_description             Current Users
            check_command                   check_nrpe!check_users
            check_period            	    24x7
            check_interval          	    9
            retry_interval          	    1
            max_check_attempts      	    5
            notification_period             24x7
            notification_options            w,u,c,r,f
            notification_interval           10
            contact_groups                  {contact_group}
    }}

        """
        total_processes_config = f"""
    define service{{

            use                             local-service
            host_name                       {host_name}
            service_description             Total Processes
            check_command                   check_nrpe!check_total_procs!350!500!RSZDT
            check_period            	    24x7
            check_interval          	    9
            retry_interval          	    1
            max_check_attempts      	    5
            notification_period             24x7
            notification_options            w,u,c,r,f
            notification_interval           10
            contact_groups                  {contact_group}
    }}

        """

        combined_config = host_config + ping_service_config + ssh_service_config \
                          + disk_usage_config + ram_usage_config + current_load_config \
                          + current_user_config + total_processes_config

        # Đặt đường dẫn tệp dựa trên yêu cầu của bạn
        # mặc định /usr/local/nagios/etc/servers
        file_path = "/usr/local/nagios/etc/servers"  # Sử dụng tiền tố 'r' để tránh xử lý đặc biệt trong đường dẫn

        # Kiểm tra xem đường dẫn tồn tại chưa, nếu không tồn tại, hãy tạo nó
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        # Đặt đường dẫn tệp cấu hình hoàn chỉnh với đuôi ".txt"
        file_path = os.path.join(file_path, file_name + ".cfg")

        with open(file_path, "w") as config_file:
            config_file.write(combined_config)
        print(
            Fore.GREEN + "---------------------------------------------------------------------------------------------")
        print(f"Successfully created configuration file for [{host_name}] and saved it to the path: [{file_path}]")
        print(
            "---------------------------------------------------------------------------------------------" + Style.RESET_ALL)

    @staticmethod
    def create_host_config_windows(host_name, alias, contact_group, ip_address, file_name):
        host_config = f"""
        ################################################################################
        # WINDOWS.CFG - SAMPLE CONFIG FILE FOR MONITORING A WINDOWS MACHINE
        #
        #
        # NOTES: This config file assumes that you are using the sample configuration
        #    files that get installed with the Nagios quickstart guide.
        #
        ################################################################################

        ################################################################################
        #                                                                              #
        #                              HOST DEFINITIONS                                #
        #                                                                              #
        ################################################################################

        # Define a host for the Windows machine we'll be monitoring
        # Change the host_name, alias, and address to fit your situation

        # Here's the definition for "Host" notifications:
        # d = send notifications on a DOWN state,
        # u = send notifications on an UNREACHABLE state,
        # r = send notifications on recoveries (OK state),
        # f = send notifications when the host starts and stops flapping,
        # s = send notifications when scheduled downtime starts and ends.

    define host{{
            use                     	windows-server
            host_name               	{host_name}
            alias                   	{alias}
            address                 	{ip_address}
            contact_groups          	{contact_group}
            check_period            	24x7
            check_command           	check-host-alive
            check_interval          	5
            retry_interval          	1
            max_check_attempts      	3
            notification_period     	24x7
            notification_options    	d,u,r,s
            notification_interval   	0
    }}

    """

        host_group = f"""
        ###############################################################################
        #                                                                             #
        #                            HOST GROUP DEFINITIONS                           #
        #                                                                             #
        ###############################################################################

        # Define a hostgroup for Windows machines
        # All hosts that use the windows-server template will automatically be a member of this group
    """
        NSClient_config = f"""
        ################################################################################
        #                                                                              #
        #                              SERVICE DEFINITIONS                             #
        #                                                                              #
        ################################################################################


        # Here's the definition for "Service" notifications:
        # w = send notifications on a WARNING state,
        # u = send notifications on an UNKNOWN state,
        # c = send notifications on a CRITICAL state,
        # r = send notifications on recoveries (OK state),
        # f = send notifications when the service starts and stops flapping,
        # s = send notifications when scheduled downtime starts and ends.

    # Create a service for monitoring the version of NSCLient++ that is installed
    # Change the host_name to match the name of the host you defined above

    define service{{
            use                             generic-service
            host_name                       {host_name}
            service_description             NSClient++ Version
            check_command                   check_nt!CLIENTVERSION
            check_period            	    24x7
            check_interval          	    5
            retry_interval          	    1
            max_check_attempts      	    3
            notification_period             24x7
            notification_options            w,u,c,r,f
            notification_interval           0
            contact_groups                  {contact_group}
    }}

        """

        up_time_config = f"""
    # Create a service for monitoring the uptime of the server
    # Change the host_name to match the name of the host you defined above

    define service{{

            use                             generic-service
            host_name                       {host_name}
            service_description             Uptime
            check_command                   check_nt!UPTIME
            check_period            	    24x7
            check_interval          	    5
            retry_interval          	    1
            max_check_attempts      	    3
            notification_period             24x7
            notification_options            w,u,c,r,f
            notification_interval           0
            contact_groups                  {contact_group}
    }}

        """

        CPU_usage_config = f"""
    # Create a service for monitoring CPU load
    # Change the host_name to match the name of the host you defined above

    define service{{

            use                             generic-service
            host_name                       {host_name}
            service_description             CPU Load
            check_command                   check_nt!CPULOAD!-l 5,80,90
            check_period            	    24x7
            check_interval          	    5
            retry_interval          	    1
            max_check_attempts      	    3
            notification_period             24x7
            notification_options            w,u,c,r,f
            notification_interval           0
            contact_groups                  {contact_group}
    }}

        """
        ram_usage_config = f"""
    # Create a service for monitoring memory usage
    # Change the host_name to match the name of the host you defined above

    define service{{

            use                             generic-service
            host_name                       {host_name}
            service_description             Memory Usage
            check_command                   check_nt!MEMUSE!-w 80 -c 90
            check_period            	    24x7
            check_interval          	    5
            retry_interval          	    1
            max_check_attempts      	    3
            notification_period             24x7
            notification_options            w,u,c,r,f
            notification_interval           0
            contact_groups                  {contact_group}
        }}

        """
        disk_space_config = f"""
    # Create a service for monitoring C:\ disk usage
    # Change the host_name to match the name of the host you defined above

    define service{{

            use                             generic-service
            host_name                       {host_name}
            service_description             C:\ Drive Space
            check_command                   check_nt!USEDDISKSPACE!-l c -w 80 -c 90
            check_period            	    24x7
            check_interval          	    5
            retry_interval          	    1
            max_check_attempts      	    3
            notification_period             24x7
            notification_options            w,u,c,r,f
            notification_interval           0
            contact_groups                  {contact_group}
    }}

        """

        combined_config = host_config + host_group + NSClient_config + up_time_config + CPU_usage_config + ram_usage_config + disk_space_config

        file_path = "/usr/local/nagios/etc/servers"

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        file_path = os.path.join(file_path, file_name + ".cfg")

        with open(file_path, "w") as config_file:
            config_file.write(combined_config)
        print(
            Fore.GREEN + "---------------------------------------------------------------------------------------------")
        print(f"Successfully created configuration file for [{host_name}] and saved it to the path: [{file_path}]")
        print(
            "---------------------------------------------------------------------------------------------" + Style.RESET_ALL)
    @staticmethod
    def create_host_config_windows_server(host_name, alias, contact_group, ip_address, file_name):
        host_config = f"""
        ################################################################################
        # WINDOWS.CFG - SAMPLE CONFIG FILE FOR MONITORING A WINDOWS MACHINE
        #
        #
        # NOTES: This config file assumes that you are using the sample configuration
        #    files that get installed with the Nagios quickstart guide.
        #
        ################################################################################

        ################################################################################
        #                                                                              #
        #                              HOST DEFINITIONS                                #
        #                                                                              #
        ################################################################################

        # Define a host for the Windows machine we'll be monitoring
        # Change the host_name, alias, and address to fit your situation

        # Here's the definition for "Host" notifications:
        # d = send notifications on a DOWN state,
        # u = send notifications on an UNREACHABLE state,
        # r = send notifications on recoveries (OK state),
        # f = send notifications when the host starts and stops flapping,
        # s = send notifications when scheduled downtime starts and ends.

    define host{{
            use                     	windows-server
            host_name               	{host_name}
            alias                   	{alias}
            address                 	{ip_address}
            contact_groups          	{contact_group}
            check_period            	24x7
            check_command           	check-host-alive
            check_interval          	15
            retry_interval          	1
            max_check_attempts      	5
            notification_period     	24x7
            notification_options    	d,u,r,s
            notification_interval   	15
    }}

    """

        host_group = f"""
        ###############################################################################
        #                                                                             #
        #                            HOST GROUP DEFINITIONS                           #
        #                                                                             #
        ###############################################################################

        # Define a hostgroup for Windows machines
        # All hosts that use the windows-server template will automatically be a member of this group
    """
        NSClient_config = f"""
        ################################################################################
        #                                                                              #
        #                              SERVICE DEFINITIONS                             #
        #                                                                              #
        ################################################################################


        # Here's the definition for "Service" notifications:
        # w = send notifications on a WARNING state,
        # u = send notifications on an UNKNOWN state,
        # c = send notifications on a CRITICAL state,
        # r = send notifications on recoveries (OK state),
        # f = send notifications when the service starts and stops flapping,
        # s = send notifications when scheduled downtime starts and ends.

    # Create a service for monitoring the version of NSCLient++ that is installed
    # Change the host_name to match the name of the host you defined above

    define service{{
            use                             generic-service
            host_name                       {host_name}
            service_description             NSClient++ Version
            check_command                   check_nt!CLIENTVERSION
            check_period            	        24x7
            check_interval          	    	15
            retry_interval          	    	1
            max_check_attempts      	    	5
            notification_period             	24x7
            notification_options            	w,u,c,r,f
            notification_interval           	15
            contact_groups                  {contact_group}
    }}

        """

        up_time_config = f"""
    # Create a service for monitoring the uptime of the server
    # Change the host_name to match the name of the host you defined above

    define service{{

            use                             generic-service
            host_name                       {host_name}
            service_description             Uptime
            check_command                   check_nt!UPTIME
            check_period            	        24x7
            check_interval          	    	15
            retry_interval          	    	1
            max_check_attempts      	    	5
            notification_period             	24x7
            notification_options            	w,u,c,r,f
            notification_interval           	15
            contact_groups                  {contact_group}
    }}

        """

        CPU_usage_config = f"""
    # Create a service for monitoring CPU load
    # Change the host_name to match the name of the host you defined above

    define service{{

            use                             generic-service
            host_name                       {host_name}
            service_description             CPU Load
            check_command                   check_nt!CPULOAD!-l 5,80,90
            check_period            	        24x7
            check_interval          	    	15
            retry_interval          	    	1
            max_check_attempts      	    	5
            notification_period             	24x7
            notification_options            	w,u,c,r,f
            notification_interval           	15
            contact_groups                  {contact_group}
    }}

        """
        ram_usage_config = f"""
    # Create a service for monitoring memory usage
    # Change the host_name to match the name of the host you defined above

    define service{{

            use                             generic-service
            host_name                       {host_name}
            service_description             Memory Usage
            check_command                   check_nt!MEMUSE!-w 80 -c 90
            check_period            	        24x7
            check_interval          	    	15
            retry_interval          	    	1
            max_check_attempts      	    	5
            notification_period             	24x7
            notification_options            	w,u,c,r,f
            notification_interval           	15
            contact_groups                  {contact_group}
        }}

        """
        disk_space_config = f"""
    # Create a service for monitoring C:\ disk usage
    # Change the host_name to match the name of the host you defined above

    define service{{

            use                             generic-service
            host_name                       {host_name}
            service_description             C:\ Drive Space
            check_command                   check_nt!USEDDISKSPACE!-l c -w 80 -c 90
            check_period            	        24x7
            check_interval          	    	15
            retry_interval          	    	1
            max_check_attempts      	    	5
            notification_period             	24x7
            notification_options            	w,u,c,r,f
            notification_interval           	15
            contact_groups                  {contact_group}
    }}

    define service{{

            use                             generic-service
            host_name                       {host_name}
            service_description             W3SVC
            check_command                   check_nt!SERVICESTATE!-d SHOWALL -l W3SVC
            check_period            	        24x7
            check_interval          	    	15
            retry_interval          	    	1
            max_check_attempts      	    	5
            notification_period             	24x7
            notification_options            	w,u,c,r,f
            notification_interval           	15
            contact_groups                  {contact_group}
    }}

    define service{{

            use                             generic-service
            host_name                       {host_name}
            service_description             Explorer
            check_command                   check_nt!PROCSTATE!-d SHOWALL -l Explorer.exe
            check_period            	        24x7
            check_interval          	    	15
            retry_interval          	    	1
            max_check_attempts      	    	5
            notification_period             	24x7
            notification_options            	w,u,c,r,f
            notification_interval           	15
            contact_groups                  {contact_group}
    }}

        """

        combined_config = host_config + host_group + NSClient_config + up_time_config + CPU_usage_config + ram_usage_config + disk_space_config

        # Đặt đường dẫn tệp dựa trên yêu cầu của bạn
        # mặc định /usr/local/nagios/etc/servers
        file_path = "/usr/local/nagios/etc/servers"  # Sử dụng tiền tố 'r' để tránh xử lý đặc biệt trong đường dẫn

        # Kiểm tra xem đường dẫn tồn tại chưa, nếu không tồn tại, hãy tạo nó
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        # Đặt đường dẫn tệp cấu hình hoàn chỉnh với đuôi ".txt"
        file_path = os.path.join(file_path, file_name + ".cfg")

        with open(file_path, "w") as config_file:
            config_file.write(combined_config)
        print(
            Fore.GREEN + "---------------------------------------------------------------------------------------------")
        print(f"Successfully created configuration file for [{host_name}] and saved it to the path: [{file_path}]")
        print(
            "---------------------------------------------------------------------------------------------" + Style.RESET_ALL)
    @staticmethod
    def create_host_config_router(host_name, alias, contact_group, ip_address, file_name,
                                  oid_port_in, oid_port_out):
        host_config = f"""
        ###############################################################################
        # ROUTER.CFG - SAMPLE CONFIG FILE FOR MONITORING A ROUTER
        #
        #
        # NOTES: This config file assumes that you are using the sample configuration
        #    files that get installed with the Nagios quickstart guide.
        #
        ###############################################################################
    
        ################################################################################
        #                                                                              #
        #                              HOST DEFINITIONS                                #
        #                                                                              #
        ################################################################################
    
        # Define the switch that we'll be monitoring
    
        # Here's the definition for "Host" notifications:
        # d = send notifications on a DOWN state,
        # u = send notifications on an UNREACHABLE state,
        # r = send notifications on recoveries (OK state),
        # f = send notifications when the host starts and stops flapping,
        # s = send notifications when scheduled downtime starts and ends.
    
    define host{{
            use                     	generic-switch
            host_name               	{host_name}
            alias                   	{alias}
            address                 	{ip_address}
            check_period            	24x7
            check_command           	check-host-alive
            check_interval          	5
            retry_interval          	1
            max_check_attempts      	3
            notification_period     	24x7
            notification_options    	d,u,r
            notification_interval   	5
            contact_groups          	{contact_group}
    
    }}
    
    """

        host_group = f"""
        ###############################################################################
        #                                                                             #
        #                            HOST GROUP DEFINITIONS                           #
        #                                                                             #
        ###############################################################################
    
    # Create a new hostgroup for switches
    
    define hostgroup {{
        hostgroup_name          Router         
        alias                   Network Router 
    }}
    
    """
        ping_service_config = f"""
        ################################################################################
        #                                                                              #
        #                              SERVICE DEFINITIONS                             #
        #                                                                              #
        ################################################################################
    
    
        # Here's the definition for "Service" notifications:
        # w = send notifications on a WARNING state,
        # u = send notifications on an UNKNOWN state,
        # c = send notifications on a CRITICAL state,
        # r = send notifications on recoveries (OK state),
        # f = send notifications when the service starts and stops flapping,
        # s = send notifications when scheduled downtime starts and ends.
    
    # Create a service to PING to router
    
    define service{{
            use                             generic-service
            host_name                       {host_name}
            service_description             PING
            check_command                   check_ping!200.0,20%!600.0,60%
            check_period            	    24x7
            check_interval          	    5
            retry_interval          	    1
            max_check_attempts      	    3
            notification_period             24x7
            notification_options            w,u,c,r,f
            notification_interval           5
            contact_groups                  {contact_group}
    }}
    
        """

        up_time_config = f"""
    # Monitor uptime via SNMP
    
    define service{{
    
            use                             generic-service
            host_name                       {host_name}
            service_description             Uptime
            check_command                   check_snmp!-C public -o sysUpTime.0
            check_period            	    24x7
            check_interval          	    5
            retry_interval          	    1
            max_check_attempts      	    3
            notification_period             24x7
            notification_options            w,u,c,r,f
            notification_interval           5
            contact_groups                  {contact_group}
    }}
    
        """

        port_1_config = f"""
    # Monitor Port 1 status via SNMP
    
    define service{{
    
            use                             generic-service
            host_name                       {host_name}
            service_description             Port 1 Link Status
            check_command                   check_snmp! -C public -o ifOperStatus.8 -r 1 -m RFC1213-MIB
            check_period            	    24x7
            check_interval          	    5
            retry_interval          	    1
            max_check_attempts      	    3
            notification_period             24x7
            notification_options            w,u,c,r,f
            notification_interval           5
            contact_groups                  {contact_group}
    }}
    
        """
        port_1_in_config = f"""
    # Monitor bandwidth via MRTG logs
    
    define service{{
    
            use                             generic-service
            host_name                       {host_name}
            service_description             Port 1 IN Bandwidth Usage
            check_command                   check_snmp!-C public -o {oid_port_in} -w 80000000 -c 100000000
            check_period            	    24x7
            check_interval          	    5
            retry_interval          	    1
            max_check_attempts      	    3
            notification_period             24x7
            notification_options            w,u,c,r,f
            notification_interval           5
            contact_groups                  {contact_group}
    }}
    
        """
        port_1_out_config = f"""
    
    define service{{
    
            use                             generic-service
            host_name                       {host_name}
            service_description             Port 1 OUT Bandwidth Usage
            check_command                   check_snmp!-C public -o {oid_port_out} -w 80000000 -c 100000000
            check_period            	    24x7
            check_interval          	    5
            retry_interval          	    1
            max_check_attempts      	    3
            notification_period             24x7
            notification_options            w,u,c,r,f
            notification_interval           5
            contact_groups                  {contact_group}
    }}
    
        """

        combined_config = host_config + host_group + ping_service_config + up_time_config \
                          + port_1_config + port_1_in_config + port_1_out_config

        # Đặt đường dẫn tệp dựa trên yêu cầu của bạn
        # mặc định /usr/local/nagios/etc/routers
        file_path = "/usr/local/nagios/etc/routers"  # Sử dụng tiền tố 'r' để tránh xử lý đặc biệt trong đường dẫn

        # Kiểm tra xem đường dẫn tồn tại chưa, nếu không tồn tại, hãy tạo nó
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        # Đặt đường dẫn tệp cấu hình hoàn chỉnh với đuôi ".txt"
        file_path = os.path.join(file_path, file_name + ".cfg")

        with open(file_path, "w") as config_file:
            config_file.write(combined_config)
        print(Fore.GREEN + "---------------------------------------------------------------------------------------------")
        print(f"Successfully created configuration file for [{host_name}] and saved it to the path: [{file_path}]")
        print(
            "---------------------------------------------------------------------------------------------" + Style.RESET_ALL)
        # image_create_success()

class edit_config_file:
    @staticmethod
    # uncomment trong file cau hinh
    def uncomment_cfg_dir_ubuntu_windows(filepath):
        updated_lines = []  # khởi tạo danh sách
        with open(filepath, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.strip().startswith('#cfg_dir=/usr/local/nagios/etc/servers'):
                    # Uncomment the line
                    updated_lines.append(line.replace('#cfg_dir=', 'cfg_dir='))
                else:
                    updated_lines.append(line)

        with open(filepath, 'w') as file:
            file.writelines(updated_lines)

    @staticmethod
    def uncomment_cfg_dir_routers(filepath):
        updated_lines = []
        with open(filepath, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.strip().startswith('#cfg_dir=/usr/local/nagios/etc/routers'):
                    # Uncomment the line
                    updated_lines.append(line.replace('#cfg_dir=', 'cfg_dir='))
                else:
                    updated_lines.append(line)

        with open(filepath, 'w') as file:
            file.writelines(updated_lines)


# các hàm kiểm tra và lọc input của người dùng
class Check_input_form:
    @staticmethod
    def is_valid_hostname(hostname):
        return re.match(r'^[a-zA-Z0-9_/.-]+( [a-zA-Z0-9_/.-]+)*$', hostname.strip()) is not None and hostname.strip() != ''

    @staticmethod
    def is_valid_group(hostname):
        return re.match(r'^[a-zA-Z0-9_/.-]+$', hostname) is not None and hostname.strip() != ''

    @staticmethod
    def is_valid_ip(ip):
        invalid_ips = {"8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1"}

        if ip in invalid_ips:
            return False

        pattern = r"^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$"

        if re.match(pattern, ip):
            parts = ip.split('.')

            for part in parts:
                if not part.isdigit() or not 0 <= int(part) <= 255:
                    return False

            first_octet = int(parts[0])

            if 1 <= first_octet <= 126:
                return True
            elif 128 <= first_octet <= 191:
                return True
            elif 192 <= first_octet <= 223:
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def check_existing_filename_servers(file_name):
        path = "/usr/local/nagios/etc/servers"
        files_in_path = os.listdir(path)

        return f"{file_name}.cfg" in files_in_path

    @staticmethod
    def is_valid_filename(filename):
        return filename and not any(char.isspace() for char in filename)

    @staticmethod
    def get_valid_input_option(input_str):
        allowed_chars = set(string.ascii_letters + ",")
        return all(char in allowed_chars for char in input_str) and not input_str.endswith(',')

    @staticmethod
    def is_valid_not_check_space(hostname):
        return re.match(r'^[a-zA-Z0-9_-]+$', hostname) is not None

    @staticmethod
    def check_oid(input_string):
        pattern = r'^(\d+\.){10}\d+$'
        if re.match(pattern, input_string):
            return True
        else:
            return False

class Check_duplicate_ips:
    @staticmethod
    def get_existing_ip_addresses(directory):
        ip_addresses = set()  # Khởi tạo một tập hợp rỗng để lưu trữ các địa chỉ IP đã được tìm thấy trong các file cấu hình
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith(".cfg"):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r') as cfg_file:
                            config_content = cfg_file.read()
                            found_ip_addresses = re.findall(r'address\s+([\d.]+)', config_content)
                            ip_addresses.update(found_ip_addresses)
        except Exception as e:
            print(f"An error occurred: {e}")
        return ip_addresses

    @staticmethod
    def check_duplicate_ips_in_cfg_files(ip_address):
        directories = ["/usr/local/nagios/etc/routers", "/usr/local/nagios/etc/servers", "/usr/local/nagios/etc/objective"]
        existing_ip_addresses = set()
        try:
            for directory in directories:
                existing_ip_addresses.update(Check_duplicate_ips.get_existing_ip_addresses(directory))

            return ip_address in existing_ip_addresses
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

class SSH:
    @staticmethod
    def execute_ssh_commands_ubuntu(ip_address, username, password, ip_to_add, commands):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(ip_address, username=username, password=password)
        except Exception as e:
            print(Fore.RED + f"\nCONNECTION FAILURE {e}" + Style.RESET_ALL)
            return

        commands_check_nscp = ["systemctl status nagios-nrpe-server"]

        result = ""
        for command in tqdm(commands_check_nscp, desc="CHECKING ...", unit=""):
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode('utf-8').strip()
            result += output + "\n"

            while not stdout.channel.exit_status_ready():
                time.sleep(1)

        found_active = any("Active: active (running)" in line for line in result.split('\n'))
        if found_active:
            print(Fore.GREEN + "\n* * * * * * * * *")
            print("Plugin installed")
            print("* * * * * * * * *\n" + Style.RESET_ALL)
        else:
            print(Fore.RED + "\n* * * * * * * * * * * * * * * * * * * * * * * * * * * *")
            print("Plugin not installed. Proceed with the installation...")
            print("* * * * * * * * * * * * * * * * * * * * * * * * * * * *\n" + Style.RESET_ALL)

            for cmd in tqdm(commands, desc="DOWNLOADING NRPE", unit=""):
                cmd_with_sudo = f'echo {password} | sudo -S {cmd}'
                ssh.exec_command(cmd_with_sudo)
                time.sleep(1)

            cmd_chmod = f'echo {password} | sudo -S chmod 777 /etc/nagios/nrpe.cfg'
            ssh.exec_command(cmd_chmod)
            time.sleep(1)

            new_config = []
            add_check_swap = False
            with ssh.open_sftp() as sftp:
                remote_file_path = '/etc/nagios/nrpe.cfg'
                with sftp.file(remote_file_path, 'r') as remote_file:
                    for line in remote_file:
                        new_config.append(line)
                        if line.startswith('command[check_hda1]=/usr/lib/nagios/plugins/check_disk'):
                            new_config.append(
                                f'#command[check_hda1]=/usr/lib/nagios/plugins/check_disk -w 20% -c 10% -p /dev/hda1\n')
                            new_config.append(
                                'command[check_hda1]=/usr/lib/nagios/plugins/check_disk -w 10% -c 5% -p /\n')
                        elif line.startswith('command[check_total_procs]=/usr/lib/nagios/plugins/check_procs'):
                            if not add_check_swap:
                                new_config.append('command[check_swap]=/usr/lib/nagios/plugins/check_swap -w 20% -c 10%\n')
                                add_check_swap = True
                        elif line.startswith('#command[check_procs]=/usr/lib/nagios/plugins/check_procs'):
                            new_config.append('command[check_procs]=/usr/lib/nagios/plugins/check_procs $ARG1$\n')

                with sftp.file(remote_file_path, 'w') as remote_file:
                    remote_file.writelines(new_config)
                    remote_file.flush()
                    remote_file.close()

            cmd1 = f'echo {password} | sudo -S sed -i "/^allowed_hosts=/s/$/, {ip_to_add}/" /etc/nagios/nrpe.cfg'
            cmd2 = f'echo {password} | sudo -S service nagios-nrpe-server restart'
            for cmd in tqdm([cmd1, cmd2], desc="CONFIGING", unit=""):
                ssh.exec_command(cmd)
                time.sleep(1)

        stdin, stdout, stderr = ssh.exec_command('hostname')
        host_name = stdout.read().decode('utf-8').strip()
        return host_name
        ssh.close()

    @staticmethod
    def execute_ssh_commands_windows(username, password, server_ip, nagios_server_ip):
        # Initialize SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the server
        try:
            ssh.connect(server_ip, username=username, password=password)
        except Exception as e:
            print(Fore.RED + f"\nCONNECTION FAILURE {e}" + Style.RESET_ALL)
            return

        commands_check_nscp = [
            "echo Test-Path HKLM:\\SYSTEM\\CurrentControlSet\\Services\\nscp > C:\\check_nscp.ps1",
            "echo If (Test-Path HKLM:\\SYSTEM\\CurrentControlSet\\Services\\nscp) { echo 'True' > C:\\check_nscp_result.txt } Else { echo 'False' > C:\\check_nscp_result.txt } >> C:\\check_nscp.ps1",
            'echo $result = Get-Content -Path "C:\\check_nscp_result.txt" >> C:\\check_nscp.ps1',
            'echo $result ^| Out-File -FilePath "C:\\result.txt" -Encoding utf8 >> C:\\check_nscp.ps1',
            'powershell -ExecutionPolicy Bypass -File "C:\\check_nscp.ps1"'
        ]
        result = ""
        for command in tqdm(commands_check_nscp, desc="CHECKING ...", unit=""):
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode('utf-8').strip()
            result += output + "\n"

            while not stdout.channel.exit_status_ready():  # Thoát vòng lặp khi exist_status nó sẵn sàng (thực hiện xong các dòng lệnh)
                time.sleep(1)

        if "True" in result:
            print(Fore.GREEN + "\n* * * * * * * * *")
            print("Plugin installed")
            print("* * * * * * * * *\n" + Style.RESET_ALL)

        else:
            print(Fore.RED + "\n* * * * * * * * * * * * * * * * * * * * * * * * * * * *")
            print("Plugin not installed. Proceed with the installation...")
            print("* * * * * * * * * * * * * * * * * * * * * * * * * * * *\n" + Style.RESET_ALL)

            commands = [
                "echo $ProgressPreference = 'SilentlyContinue' > C:\\install_nscp.ps1",
                "echo Invoke-WebRequest -Uri 'https://github.com/mickem/nscp/releases/download/0.5.2.41/NSCP-0.5.2.41-Win32.msi' -OutFile 'C:\\NSCP-0.5.2.41-Win32.msi' >> C:\\install_nscp.ps1",
                "echo Start-Process -Wait -FilePath 'msiexec' -ArgumentList '/i C:\\NSCP-0.5.2.41-Win32.msi /quiet /norestart' >> C:\\install_nscp.ps1",
                "echo $nsclientIniPath = 'C:\\Program Files (x86)\\NSClient++\\nsclient.ini' >> C:\\install_nscp.ps1",
                f"echo $additionalConfig = '; in flight - TODO' + [Environment]::NewLine + '[/settings/default]' + [Environment]::NewLine + '; Undocumented key' + [Environment]::NewLine + 'allowed hosts = {nagios_server_ip}' + [Environment]::NewLine + '; in flight - TODO' + [Environment]::NewLine + '[/settings/NRPE/server]' + [Environment]::NewLine + '; Undocumented key' + [Environment]::NewLine + 'verify mode = none' + [Environment]::NewLine + '; Undocumented key' + [Environment]::NewLine + 'insecure = true' + [Environment]::NewLine + '; in flight - TODO' + [Environment]::NewLine + '[/modules]' + [Environment]::NewLine + '; Undocumented key' + [Environment]::NewLine + 'CheckSystem = disabled' + [Environment]::NewLine + '; Undocumented key' + [Environment]::NewLine + 'NSClientServer = enabled' + [Environment]::NewLine + '; Undocumented key' + [Environment]::NewLine + 'NRPEServer = enabled' + [Environment]::NewLine + 'CheckExternalScripts = 1' + [Environment]::NewLine + 'CheckHelpers = 1' + [Environment]::NewLine + 'CheckEventLog = 1' + [Environment]::NewLine + 'CheckNSCP = 1' + [Environment]::NewLine + 'CheckDisk = 1' + [Environment]::NewLine + 'CheckSystem = 1' + [Environment]::NewLine >> C:\\install_nscp.ps1",
                "echo Set-Content -Path $nsclientIniPath -Value $additionalConfig >> C:\\install_nscp.ps1",
                "echo $nsclientIniContent += $additionalConfig >> C:\\install_nscp.ps1",
                "echo $nsclientIniContent ^| Set-Content -Path $nsclientIniPath >> C:\\install_nscp.ps1",
                "echo Get-Content -Path $nsclientIniPath >> C:\\install_nscp.ps1",
                "echo Restart-Service -Name 'nscp' >> C:\\install_nscp.ps1",
            ]

            # Execute PowerShell script from file
            for command in tqdm(commands, desc="REPAIRING...", unit=""):
                stdin, stdout, stderr = ssh.exec_command(command)
            while not stdout.channel.exit_status_ready():  # Wait until the command completes
                time.sleep(1)

            commands_execute = [
                'powershell -ExecutionPolicy Bypass -File "C:\\install_nscp.ps1"']
            for command in tqdm(commands_execute, desc="INSTALLING...", unit=""):
                stdin, stdout, stderr = ssh.exec_command(command)
            while not stdout.channel.exit_status_ready():  # Wait until the command completes
                time.sleep(1)

        stdin, stdout, stderr = ssh.exec_command('hostname')
        host_name = stdout.read().decode('utf-8').strip()
        return host_name
        ssh.close()

# hàm nhập
class input_info:
    @staticmethod
    def input_server_info_linux():
        # Check alias
        alias = input("Enter alias name: ")
        while not Check_input_form.is_valid_hostname(alias):
            print("Invalid alias. Please re-enter.")
            print("Does not contain special characters and is not empty \n")
            alias = input("Enter alias name: ")

        # Check contact_group
        contact_group = input("Enter a contact group name: ")
        print(" ")
        while not Check_input_form.is_valid_group(contact_group):
            print("Invalid contact group. Please re-enter.")
            print("Does not contain special characters and is not empty \n")
            contact_group = input("Enter a contact group name: ")

        # Check IP
        ip_address = input("Enter IP address: ")
        print(" ")
        while Check_duplicate_ips.check_duplicate_ips_in_cfg_files(ip_address):
            print("The IP address was used. Please re-enter.")
            ip_address = input("Enter IP address: ")
            print(" ")
        while not Check_input_form.is_valid_ip(ip_address):
            print("The IP address is not properly formatted and not enter IP DNS. Please re-enter.")
            print("Class A: 1.0.0.0 - 126.255.255.255\n"
                  "Class B: 128.0.0.0 - 191.255.255.255\n"
                  "Class C: 192.0.0.0 - 223.255.255.255\n")
            ip_address = input("Enter IP address: ")
            print(" ")

        print(Fore.CYAN + "\n---------------------------------------------------")
        print("### CREATE TEST SESSION AND INSTALL NRPE CLIENT ###")
        print("---------------------------------------------------\n" + Style.RESET_ALL)
        username = input("Enter username: ")
        while not Check_input_form.is_valid_filename(username):
            print("Do not empty username !\n")
            username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        # Danh sách các lệnh bạn muốn thực hiện
        commands = ["sudo apt update -y", "sudo apt install nagios-nrpe-server -y",
                    "sudo apt install nagios-plugins -y"]
        # Thêm địa chỉ IP vào allowed_hosts trong nrpe.cfg
        ip_to_add = input("Enter IP nagios server: ")
        while not Check_input_form.is_valid_ip(ip_to_add):
            print("The IP address is not properly formatted and not enter IP DNS. Please re-enter.")
            print("Class A: 1.0.0.0 - 126.255.255.255\n"
                  "Class B: 128.0.0.0 - 191.255.255.255\n"
                  "Class C: 192.0.0.0 - 223.255.255.255\n")
            ip_to_add = input("Enter IP nagios server: ")
            print(" ")
        host_name = SSH.execute_ssh_commands_ubuntu(ip_address, username, password, ip_to_add, commands)

        # Check ten file
        if host_name is not None:
            file_name = input("Enter a name for the configuration file [ex: ubuntu,windows,router]: ")
            file_name_with_extension = f"{file_name}.cfg"  # Tên file với đuôi .cfg

            path = "/usr/local/nagios/etc/servers/" + file_name_with_extension  # Đường dẫn đầy đủ tới file

            while os.path.exists(path) or Check_input_form.check_existing_filename_servers(file_name):
                print("File name already exists. Please enter a different name.")
                file_name = input("Enter a name for the configuration file [ex: ubuntu,windows,router]: ")
                file_name_with_extension = f"{file_name}.cfg"
                path = "/usr/local/nagios/etc/servers/" + file_name_with_extension  # Cập nhật lại đường dẫn khi nhập lại tên file

            while not Check_input_form.is_valid_filename(file_name):
                print("Invalid filename. Please re-enter.")
                print("Does not contain special characters and is not empty \n")
                file_name = input("Enter a name for the configuration file [ex: ubuntu,windows,router]: ")
                print(" ")
        else:
            print(Fore.RED + "FAIL TO SAVE CONFIG FILE" + Style.RESET_ALL)
            print(Fore.CYAN + "\n# PLEASE TRY AGAIN #\n" + Style.RESET_ALL)
            print(Fore.CYAN + "RE-ENTER YOUR LINUX DEVICE INFORMATION" + Style.RESET_ALL)
            return input_info.input_server_info_linux()

        return host_name, alias, contact_group, ip_address, file_name
    @staticmethod
    def input_server_info_windows():
        # Check alias
        alias = input("Enter alias name: ")
        while not Check_input_form.is_valid_hostname(alias):
            print("Invalid alias. Please re-enter.")
            print("Does not contain special characters and is not empty \n")
            alias = input("Enter alias name: ")

        # Check contact_group
        contact_group = input("Enter contact group name: ")
        print(" ")
        while not Check_input_form.is_valid_group(contact_group):
            print("Invalid contact group. Please re-enter.")
            print("Does not contain special characters and is not empty \n")
            contact_group = input("Enter contact group name: ")

        # Check IP
        ip_address = input("Enter IP address: ")
        print(" ")
        while Check_duplicate_ips.check_duplicate_ips_in_cfg_files(ip_address):
            print("The IP address was used. Please re-enter.")
            ip_address = input("Enter IP address: ")
            print(" ")
        while not Check_input_form.is_valid_ip(ip_address):
            print("The IP address is not properly formatted and not enter IP DNS. Please re-enter.")
            print("Class A: 1.0.0.0 - 126.255.255.255\n"
                  "Class B: 128.0.0.0 - 191.255.255.255\n"
                  "Class C: 192.0.0.0 - 223.255.255.255\n")
            ip_address = input("Nhập địa chỉ IP: ")
            print(" ")
        print(Fore.CYAN + "\n---------------------------------------------------")
        print("### CREATE A TEST SESSION AND INSTALL NSClient++ CLIENT ###")
        print("---------------------------------------------------" + Style.RESET_ALL)
        username = input("Enter username: ")
        while not Check_input_form.is_valid_filename(username):
            print("Do not empty username \n")
            username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        # Thêm địa chỉ IP vào allowed_hosts trong nsclient.ini
        nagios_server_ip = input("Enter IP nagios server: ")
        while not Check_input_form.is_valid_ip(nagios_server_ip):
            print("The IP address is not properly formatted and not enter IP DNS. Please re-enter.")
            print("Class A: 1.0.0.0 - 126.255.255.255\n"
                  "Class B: 128.0.0.0 - 191.255.255.255\n"
                  "Class C: 192.0.0.0 - 223.255.255.255\n")
            nagios_server_ip = input("Enter IP nagios server: ")
            print(" ")
        host_name = SSH.execute_ssh_commands_windows(username, password, ip_address, nagios_server_ip)

        # Check ten file
        if host_name is not None:
            file_name = input("Enter a name for the configuration file [ex: ubuntu,windows,router]: ")
            file_name_with_extension = f"{file_name}.cfg"  # Tên file với đuôi .cfg

            path = "/usr/local/nagios/etc/servers/" + file_name_with_extension  # Đường dẫn đầy đủ tới file

            while os.path.exists(path) or Check_input_form.check_existing_filename_servers(file_name):
                print("File name already exists. Please enter a different name.")
                file_name = input("Enter a name for the configuration file [ex: ubuntu,windows,router]: ")
                file_name_with_extension = f"{file_name}.cfg"
                path = "/usr/local/nagios/etc/servers/" + file_name_with_extension  # Cập nhật lại đường dẫn khi nhập lại tên file

            while not Check_input_form.is_valid_filename(file_name):
                print("Invalid filename. Please re-enter.")
                print("Does not contain special characters and is not empty \n")
                file_name = input("Enter a name for the configuration file [ex: ubuntu,windows,router]: ")
                print("")
        else:
            print(Fore.RED + "FAIL TO SAVE CONFIG FILE" + Style.RESET_ALL)
            print(Fore.CYAN + "\n# PLEASE TRY AGAIN #\n" + Style.RESET_ALL)
            print(Fore.CYAN + "RE-ENTER YOUR WINDOWS DEVICE INFORMATION" + Style.RESET_ALL)
            return input_info.input_server_info_windows()

        return host_name, alias, contact_group, ip_address, file_name

    @staticmethod

    def input_server_info_router():
        # Check hostname
        host_name = input("Enter a server name: ")
        while not Check_input_form.is_valid_hostname(host_name):
            print("Invalid hostname. Please re-enter.")
            print("Does not contain special characters and is not empty \n")
            host_name = input("Enter server name: ")

        # Check alias
        alias = input("Enter alias name: ")
        while not Check_input_form.is_valid_hostname(alias):
            print("Invalid alias. Please re-enter.")
            print("Does not contain special characters and is not empty \n")
            alias = input("Enter alias name: ")

        # Check contact_group
        contact_group = input("Enter a contact group name: ")
        print(" ")
        while not Check_input_form.is_valid_group(contact_group):
            print("Invalid contact group. Please re-enter.")
            print("Does not contain special characters and is not empty \n")
            contact_group = input("Enter contact group name: ")

        # Check IP
        ip_address = input("Enter IP address: ")
        print(" ")
        while not Check_input_form.is_valid_ip(ip_address):
            print("The IP address is not properly formatted and not enter IP DNS. Please re-enter.")
            print("Class A: 1.0.0.0 - 126.255.255.255\n"
                  "Class B: 128.0.0.0 - 191.255.255.255\n"
                  "Class C: 192.0.0.0 - 223.255.255.255\n")
            ip_address = input("Enter IP address: ")
            print(" ")

        # Check ten file
        file_name = input("Enter a name for the configuration file [Example: ubuntu,windows,router]: ")
        print(" ")
        while not Check_input_form.is_valid_filename(file_name):
            print("Invalid filename. Please re-enter.")
            print("Does not contain special characters and is not empty \n")
            file_name = input("Enter a name for the configuration file [Example: ubuntu,windows,router]: ")
            print(" ")

        # Tham số OID IN Bandwidth Usage
        oid_port_in = input("Enter the OID parameter <Port 1 IN Bandwidth Usage> [DEFAULT: 1.3.6.1.2.1.2.2.1.16.8]: ")
        if not oid_port_in:
            print("[DEFAULT]")
            oid_port_in = '1.3.6.1.2.1.2.2.1.16.8'
        while not Check_input_form.check_oid(oid_port_in):
            print("The OID is invalid. Please re-enter.")
            print("Does not contain special characters and is not empty \n")
            oid_port_in = input("Enter OID <Port 1 IN Bandwidth Usage> [DEFAULT: 1.3.6.1.2.1.2.2.1.16.8]: ")
            if not oid_port_in:
                print("[DEFAULT]")
                oid_port_in = '1.3.6.1.2.1.2.2.1.16.8'

        # Tham số OID OUT Bandwidth Usage
        oid_port_out = input("Enter the OID parameter <Port 1 OUT Bandwidth Usage> [DEFAULT: 1.3.6.1.2.1.2.2.1.10.8]: ")
        if not oid_port_out:
            print("[DEFAULT]")
            oid_port_out = '1.3.6.1.2.1.2.2.1.10.8'
        while not Check_input_form.check_oid(oid_port_out):
            print("The OID is invalid. Please re-enter.")
            print("Does not contain special characters and is not empty \n")
            oid_port_out = input("Enter the OID parameter <Port 1 OUT Bandwidth Usage> [DEFAULT: 1.3.6.1.2.1.2.2.1.10.8]: ")
            if not oid_port_out:
                print("[DEFAULT]")
                oid_port_out = '1.3.6.1.2.1.2.2.1.10.8'

        return host_name, alias, contact_group, ip_address, file_name, oid_port_in, oid_port_out


def menu():
    print("   _   ___  ___     ___ ___  _  _ ___ ___ ___       ")
    print("  /_\\ |   \\|   \\   / __/ _ \\| \\| | __|_ _/ __|  ___ ")
    print(" / _ \\| |) | |) | | (_| (_) | .` | _| | | (_ | |___|")
    print("/_/ \\_\\___/|___/   \\___\\___/|_|\\_|_| |___\\___|      ")
    print("                                                   ")
    print(" _  _   _   ___ ___ ___  ___                          ")
    print("| \\| | /_\\ / __|_ _/ _ \\/ __|                        ")
    print("| .` |/ _ \\ (_ || | (_) \\__ \\                        ")
    print("|_|\\_/_/ \\_\\___|___\\___/|___/                        ")
    print("")
    # text = "ADD CONFIG - NAGIOS"
    # ascii_art = pyfiglet.figlet_format(text, font="small")
    # print(ascii_art)
    print("")
    print("[1]       LINUX              \n")
    print("[2]       WINDOWS CLIENT     \n")
    print("[3]       ROUTER             \n")
    print("[4]       WINDOWS SERVER     \n")
    print("[0]       EXIT              ")


if __name__ == "__main__":
    main()
