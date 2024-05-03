# Runs Exhaustive Matching by default
`python3 Sphere_Sfm_runner.py --name <project_name>`


# Runs Vocab Tree Matching 
`python3 Sphere_Sfm_runner.py --name <project_name> --feature_matcher v
`

# Runs Spatial Matching 
`python3 Sphere_Sfm_runner.py -s <s3_path>/images/ --name <project_name> --feature_extractor pos --feature_matcher s
`