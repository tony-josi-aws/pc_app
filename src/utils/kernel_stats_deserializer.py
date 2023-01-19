from tabulate import tabulate


class KernelStats(object):
    def __init__(self) -> None:
        self.all_tasks_stats = []

    def append(self, one_task_stats):
        self.all_tasks_stats.append(one_task_stats)

    def get_all_task_stats(self):
        return self.all_tasks_stats

    def __str__(self) -> str:
        table_header = ['Task Name', 'CPU Time', 'CPU %']
        return tabulate(self.all_tasks_stats, headers=table_header, tablefmt="grid")


def deserialize_kernel_stats(network_stats_str):
    tasks = network_stats_str.split("\r\n")
    tasks = list(filter(None, tasks)) # Remove empty entries

    deserialized_kernel_stats = KernelStats()

    for task in tasks:
        task_stats = task.split("\t")
        task_stats = list(filter(None, task_stats)) # Remove empty entries
        task_name = task_stats[0].strip()
        task_cpu_time = task_stats[1].strip()
        task_cpu_pct = task_stats[2].strip()
        deserialized_kernel_stats.append([task_name, task_cpu_time, task_cpu_pct])

    return deserialized_kernel_stats
