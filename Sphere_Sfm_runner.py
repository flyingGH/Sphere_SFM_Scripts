import os
import subprocess
import sys
import argparse
import time
import smtplib
from email.mime.text import MIMEText
import socket
import glob

SENDER = "akileswar.paidi@constructn.ai"
RECIPIENTS = [SENDER, "anirudh.kakarlapudi@constructn.ai","pradeep.borugadda@constructn.ai"]
PASSWORD = "wkto ivvo iepi xkjy"

def get_server_name():
    server_name = socket.gethostname()
    return server_name

def run_du_command():
    directories = glob.glob('colmap/sparse/*/')
    
    if not directories:
        print("No directories found.")
        return

    command = ['du', '-h'] + directories
    
    result = subprocess.run(command, text=True, capture_output=True)
    
    if result.returncode == 0:
        print("Command executed successfully:\n", result.stdout)
        return result.stdout
    else:
        print("Failed to execute command:", result.stderr)
        return 0
    
def send_email(subject, body, sender=SENDER,
               recipients=RECIPIENTS, password=PASSWORD):
    """ Sends the email from the sender to recipients
    Args:
        subject(str):
            The subject of the email
        body(str):
            The body of the email
        sender(str):
            The sender of the email(gmail)
        recipeients(list):
            List of email ids of the recipients
        password(str):
            Password for the sender email
    """
    if type(body) == type({}):
        body_text = ""
        for key, value in body.items():
            text = f"\n{key}\t:\t{value}\n"
            body_text += text
    elif type(body) == type("1"):
        body_text = body
    else:
        body = None
    msg = MIMEText(body_text)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

def check_files(*files):
    """ Check if all files in the list exist. """
    missing = [file for file in files if not os.path.exists(file)]
    if missing:
        raise FileNotFoundError(f"Missing required files: {', '.join(missing)}")

def handle_local_files():
    original_dir = os.getcwd() 
    print("YOU ARE AT ",original_dir)
    try:
        os.chdir('images')

        if os.path.exists('thumbnails'):
            subprocess.run(['rm', '-rf', 'thumbnails'], check=True)

        if os.path.exists('boundary.json'):
            os.remove('boundary.json')

        if os.path.exists('geo.txt'):
            subprocess.run(['mv', 'geo.txt', '..'], check=True)

    finally:
        os.chdir(original_dir) 
        print("FINALLY YOU ARE AT ",original_dir)
    
def main(args):
    start_time = time.time() 

    s3_path = args.s3_folder_path
    aws_command = f"aws s3 sync {s3_path} ./images/"
    subprocess.run(aws_command, check=True, shell=True)

    handle_local_files()

    os.environ['DISPLAY'] = ':99.0'
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'
    subprocess.Popen("Xvfb :99 &", shell=True)

    out_path = "./colmap/sparse"
    ba_out_path = "./colmap/sparse_ba"

    os.makedirs(out_path, exist_ok=True)
    os.makedirs(os.path.join(ba_out_path, "0"), exist_ok=True)
    os.makedirs(os.path.join(ba_out_path, "1"), exist_ok=True)
  
    subprocess.run("colmap database_creator --database_path ./colmap/database.db", shell=True)

    try:
        command = "python3 add_identity_spatial.py"
        subprocess.run([command],check=True , shell = True)
        print("POS.txt generated successfully")
    except subprocess.CalledProcessError:
        print("Failed to generate POS.txt")
    except Exception as e:
        print(f"An error occurred: {e}")

    base_cmd = f"colmap feature_extractor --database_path ./colmap/database.db --image_path ./images --ImageReader.camera_model SPHERE --ImageReader.camera_params '1,2048,1024' --ImageReader.single_camera 1"
    if args.feature_extractor == 'pos':
        check_files('./POS.txt')
        subprocess.run(base_cmd + " --ImageReader.pose_path ./POS.txt", shell=True)
    elif args.feature_extractor == 'posNmask':
        check_files('./POS.txt', './camera_mask.png')
        subprocess.run(base_cmd + " --ImageReader.camera_mask_path ./camera_mask.png --ImageReader.pose_path ./POS.txt", shell=True)
    else:
        subprocess.run(base_cmd, shell=True)

    image_count = int(subprocess.getoutput("ls ./images/*.JPG | wc -l"))
    vocab_tree_path = "./vocab_tree_flickr100K_words32K.bin" if image_count < 1000 else "./vocab_tree_flickr100K_words256K.bin"
    wget_command = f"wget https://demuc.de/colmap/{os.path.basename(vocab_tree_path)}"
    subprocess.run(wget_command, shell=True)

    if args.feature_matcher == 's':
        subprocess.run(f"time colmap spatial_matcher --database_path ./colmap/database.db --SiftMatching.max_error 4 --SiftMatching.min_num_inliers 50 --SpatialMatching.is_gps 0 --SpatialMatching.max_distance 50", shell=True)
    elif args.feature_matcher == 'v':
        subprocess.run(f"time colmap vocab_tree_matcher --database_path ./colmap/database.db --SiftMatching.max_error 4 --SiftMatching.min_num_inliers 50 --VocabTreeMatching.vocab_tree_path {vocab_tree_path}", shell=True)
    elif args.feature_matcher == 'e':
        subprocess.run("time colmap exhaustive_matcher --database_path ./colmap/database.db --SiftMatching.max_error 4 --SiftMatching.min_num_inliers 50", shell=True)

    subprocess.run("time colmap mapper --database_path ./colmap/database.db --image_path ./images --output_path ./colmap/sparse --Mapper.ba_refine_focal_length 0 --Mapper.ba_refine_principal_point 0 --Mapper.ba_refine_extra_params 0 --Mapper.sphere_camera 1", shell=True)

    end_time = time.time()
    total_time = end_time - start_time
    total_minutes = total_time / 60
    print(f"=====> Total Time Taken <======= : {total_minutes:.2f} minutes")


    experiment_name = args.name
    server_name = get_server_name()
    sparse_command = "find colmap/sparse/ -mindepth 1 -maxdepth 1 -type d | wc -l"
    sparse_process = subprocess.run(sparse_command, shell=True, text=True, capture_output=True)
    no_of_sparse = sparse_process.stdout.strip()
    sparse_directory_sizes = run_du_command()

    subject = f"SphereSFM of data {experiment_name} completed successfully in Server {server_name} "
    body = (
            f"Processing of dataset {args.name} completed successfully on {socket.gethostname()}.\n\n"
            f"Time Taken: {total_minutes:.2f} minutes\n"
            f"Image Count: {image_count}\n"
            f"No of Sparse Files: {no_of_sparse}\n"
            f"Directory Sizes:\n{sparse_directory_sizes}"
        )
    send_email(subject,body,SENDER,RECIPIENTS,PASSWORD)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run COLMAP processing with variable options.")
    
    parser.add_argument("-s", "--s3_folder_path", required=True,
                        help="AWS path for the s3 folder that contains" +
                             "images, boundary.geojson, output_path.json")
    
    parser.add_argument("-n", "--name", type=str, default="colmap_output", help="Name of the dataset to process")

    parser.add_argument('--feature_extractor', choices=['normal', 'pos', 'posNmask'], default='normal',
                        help='Feature extractor mode: normal, pos (uses POS.txt), posNmask (uses POS.txt and camera_mask.png)')
    
    parser.add_argument('--feature_matcher', choices=['s', 'v', 'e'], default='e',
                        help='Feature matcher mode: s (spatial), v (vocab tree), e (exhaustive)')
    
    args = parser.parse_args()

    try:
        main(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
