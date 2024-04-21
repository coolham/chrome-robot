import os
import sys
import shutil
import subprocess
import platform
import pylnk3
sys.path.append('../../')
sys.path.append(os.getcwd()) 
import argparse
from utils.config import MasterConfig
from utils.logger_factory import create_logger


def generate_browsers(num_browsers, profile_name_prefix, template_profile, browser_profile_dirs, delete_exist=False):
    logger = create_logger(log_prefix='browsers', log_level='info')
    logger.info(f'Generating {num_browsers} browsers with custom profiles')
    current_dir = os.getcwd()
    if delete_exist:
        if os.path.exists(browser_profile_dirs):
            shutil.rmtree(browser_profile_dirs)
    user_data_base = os.path.join(current_dir, browser_profile_dirs, 'User Data')
    os.makedirs(user_data_base, exist_ok=True)

    for i in range(num_browsers):
        # specify profile name, such as: profile0001, profile0002, ...
        profile_name = f'{profile_name_prefix}{i+1:04d}'
        profile_dir = os.path.join(user_data_base, profile_name)
        logger.info(f'Generating browser with profile: {profile_name}')
        logger.info(f'Profile directory: {profile_dir}')
        shutil.copytree(template_profile, profile_dir)

        if platform.system().lower() == 'windows':
            # user_data_dir = os.path.join(profile_dir, 'User Data', 'Default')
            preferences_file = os.path.join(template_profile, 'Preferences')
            with open(preferences_file, 'r') as f:
                preferences = f.read()

            modified_preferences = preferences.replace('user_data_dir": "\\Default"', f'user_data_dir": "{profile_dir}"')

            with open(preferences_file, 'w') as f:
                f.write(modified_preferences)

           
            # chrome_command = ['chrome', '--user-data-dir', user_data_dir]
            # chrome_command = ['C:\Program Files\Google\Chrome\Application\chrome.exe', f'--user-data-dir="{user_data_dir}"', f'--profile-directory="{profile_name}"']
            # chrome_command = ['C:\Program Files\Google\Chrome\Application\chrome.exe', '--user-data-dir', f'"{user_data_dir}"', '--profile-directory', f'"{profile_name}"', '--new-window']
            # chrome_command = f'"C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="{user_data_dir}" --profile-directory="{profile_name}"'
            short_cut_dir = os.path.join(current_dir, browser_profile_dirs, 'short_cut')
            create_windows_shortcut(short_cut_dir, browser_profile_dirs, profile_dir, profile_name)

        elif platform.system().lower() == 'linux':
            user_data_dir = os.path.join(profile_dir, 'Default')
            preferences_file = os.path.join(user_data_dir, 'Preferences')
            with open(preferences_file, 'r') as f:
                preferences = f.read()

            modified_preferences = preferences.replace('user-data-dir": "Default"', f'user_data_dir": "{profile_dir}"')

            with open(preferences_file, 'w') as f:
                f.write(modified_preferences)

            chrome_command = ['google-chrome', '--user-data-dir', profile_dir]
        else:
            raise ValueError(f'Unsupported operating system: {platform.system()}')

def create_windows_shortcut(short_cut_dir, browser_profile_dirs, user_data_dir, profile_name):
    if not os.path.exists(short_cut_dir):
        os.makedirs(short_cut_dir)
    lnk_name = os.path.join(short_cut_dir, profile_name + '.lnk')
    target_file = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    icon_f = os.path.join(user_data_dir, 'Google Profile.ico')
    args = f'--user-data-dir="{user_data_dir}" --profile-directory="{profile_name}"'
    window_m = pylnk3.WINDOW_NORMAL
    work_dir = user_data_dir
    # 创建lnk文件
    pylnk3.for_file(target_file=target_file, lnk_name=lnk_name,
                arguments=args,description="chrome ",icon_file=icon_f,
                icon_index=0, work_dir=work_dir, window_mode=window_m)
    # 解析生成的lnk文件
    with open(lnk_name,"rb") as fdata:
        lnk = pylnk3.parse(fdata)
        print(lnk)

def create_linux_desktop_entry(profile_dir, profile_name):
    desktop_entry_path = os.path.join(profile_dir, profile_name + '.desktop')
    with open(desktop_entry_path, 'w') as f:
        f.write('[Desktop Entry]\n')
        f.write('Type=Application\n')
        f.write(f'Exec="[CHROME_PATH]" --user-data-dir="{profile_dir}" --profile-directory="{profile_name}"\n')
        f.write('Icon=[ICON_PATH]\n')  # Optional: Path to an icon
        f.write('Terminal=false\n')
        f.write(f'Name={profile_name}\n')
        f.write(f'Comment=[PROFILE_DESCRIPTION]\n')  # Optional: Description
        f.write('Categories=WebBrowser;\n')

if __name__ == '__main__':
    # cur_dir = os.path.dirname(os.path.basename(__file__))
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.abspath(os.path.join(cur_dir, '..')) 
    print('base_dir:', base_dir)

    logger = create_logger(log_prefix='browsers', log_level='info')

    parser = argparse.ArgumentParser(description='Serial port communication test program')
    # parser.add_argument('--force', type=bool, default=False, help='delete exist chrome profile')
    parser.add_argument('--force', type=bool, default=True, help='delete exist chrome profile')

    args = parser.parse_args()

    num_browsers = 3  # Specify the number of browsers to generate
    profile_name_prefix = 'profile'  # Prefix for custom profile names
    config_file = os.path.join(base_dir, 'conf', 'config.yaml')
    config = MasterConfig(config_file=config_file)

    # Path to the template browser directory
    template_profile = config.get_config('chrome', 'template', 'profile')  
    # template_dir = '/path/to/template/browser/directory'  # Path to the template browser directory

    browser_profile_dirs = config.get_config('browser', 'profiles_dir')
    generate_browsers(num_browsers, profile_name_prefix, template_profile, browser_profile_dirs, args.force)
