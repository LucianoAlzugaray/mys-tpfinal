FROM jupyter/scipy-notebook
COPY MyS_tp_final.ipynb  ${HOME}
EXPOSE 8888
