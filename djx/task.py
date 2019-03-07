from djx.utils import get_method, get_all_data, store_data


def run(task):
    entry = task['entry']
    output_prefix = task['result']['prefix']
    data = get_all_data(task['data'])
    func = get_method(entry)
    output_files, result = func(*data, **task['params'])
    remote_output_files = store_data(output_files, output_prefix)
    return {
        **task, 'output_files': remote_output_files, 'result': result
    }
