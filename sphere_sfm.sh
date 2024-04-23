# Setup platform
export DISPLAY=":99.0" \
export QT_QPA_PLATFORM="offscreen" \
Xvfb :99 &

# 0
export out_path="./colmap/sparse" \
export ba_out_path="./colmap/sparse_ba" 

mkdir -p "$out_path" \
mkdir -p "$ba_out_path/0" \
mkdir -p "$ba_out_path/1" 

# 1
colmap database_creator --database_path ./colmap/database.db

# 2
time colmap feature_extractor \
    --database_path ./colmap/database.db \
    --image_path ./images \
    --ImageReader.camera_model SPHERE \
    --ImageReader.camera_params "1,2048,1024" \
    --ImageReader.single_camera 1

time colmap feature_extractor \
    --database_path ./colmap/database.db \
    --image_path ./images \
    --ImageReader.camera_model SPHERE \
    --ImageReader.camera_params "1,2048,1024" \
    --ImageReader.single_camera 1 \
    --ImageReader.pose_path ./POS.txt

time colmap feature_extractor \
    --database_path ./colmap/database.db \
    --image_path ./images \
    --ImageReader.camera_model SPHERE \
    --ImageReader.camera_params "1,2048,1024" \
    --ImageReader.single_camera 1 \
    --ImageReader.camera_mask_path ./camera_mask.png \
    --ImageReader.pose_path ./POS.txt

# 3

time colmap spatial_matcher \
    --database_path ./colmap/database.db \
    --SiftMatching.max_error 4 \
    --SiftMatching.min_num_inliers 50 \
    --SpatialMatching.is_gps 0 \
    --SpatialMatching.max_distance 50

time colmap vocab_tree_matcher \
    --database_path ./colmap/database.db \
    --SiftMatching.max_error 4 \
    --SiftMatching.min_num_inliers 50 \
    --VocabTreeMatching.vocab_tree_path ./vocab_tree_flickr100K_words32K.bin

time colmap exhaustive_matcher \
    --database_path ./colmap/database.db \
    --SiftMatching.max_error 4 \
    --SiftMatching.min_num_inliers 50 \ 

# 4
    
time colmap mapper \
    --database_path ./colmap/database.db \
    --image_path ./images \
    --output_path ./colmap/sparse \
    --Mapper.ba_refine_focal_length 0 \
    --Mapper.ba_refine_principal_point 0 \
    --Mapper.ba_refine_extra_params 0 \
    --Mapper.sphere_camera 1 \

time colmap mapper \
    --database_path "$database_path" \
    --image_path "$image_path" \
    --output_path "$out_path" \
    --Mapper.ba_global_function_tolerance=0.000001

# 5 
 mkdir -p test && colmap model_converter --input_path 0 --output_path test --output_type TXT