dvc run -f {dvc_file} -d {python_file} -d {job_file} \
    -o {out_path} \
    python {python_file} {job_file} {out_path} > {log_file}