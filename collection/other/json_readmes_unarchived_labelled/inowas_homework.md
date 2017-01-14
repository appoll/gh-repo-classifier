# Homework
the modflow homework repository

## Installation of modflow image

Navigate to the homework-folder and type the following to install the image:

```shell
docker build -t inowas/modflow .
```

For the installation you will need a internet connection and some time.
The commandline will fill with many lines of logs.

[Here the logs of the installation on mac](./log_docker_modflow_image_installation.log)

## Run the modflow example

```shell
docker run -t -v $(pwd)/data:/data inowas/modflow python lake_example.py
```

After executing the example a bunch of new files will be generated in the data/output - folder.  
You can delete this folder and execute the script again and again.

