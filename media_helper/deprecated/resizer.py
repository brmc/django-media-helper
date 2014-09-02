def resize_all(media_root, width):
    """ Resizes all images in upload directories for a new screen width

    :param root MEDIA_ROOT
    :param width: a string representation of an integer
    """

    new_size = Settings().generate_scaling_factors([width,]) 
    upload_dirs = find_field_attribute("upload_to", *find_models_with_field(models.ImageField))
    
    # This block iterates through upload_to directories, each sub directory,
    # and finally resizes each file.
    for upload_dir in upload_dirs:
        # Source dir from which images will be resized
        source_dir = os.path.join(media_root, upload_dir)
        
        if os.path.isdir(source_dir):
            # The directory for the newly scaled images
            resize_dir = os.path.join(media_root, width, upload_dir)
            create_directories(media_root, upload_dir)
            
            for subdir, dirs, files in os.walk(source_dir):
                for file in files:
                    new_file = os.path.join(resize_dir, upload_dir, file)
                    
                    if not os.path.isfile(new_file):
                        image_path = os.path.join(subdir, file)
                        
                        resize(media_root, new_size.keys()[0], new_size.values()[0], image_path)
