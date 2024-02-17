# cd ~/dev/nmt-models/.venv/lib/python3.10/site-packages/tensorrt_libs
# ln -s libnvinfer_plugin.so.8 libnvinfer_plugin.so.7
# ln -s libnvinfer.so.8 libnvinfer.so.7
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/dev/nmt-models/.venv/lib/python3.10/site-packages/tensorrt_libs
