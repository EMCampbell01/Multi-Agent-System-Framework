from collections import defaultdict

class Memory():
    
    def __init__(self) -> None:
        self.default_particion_size = 25
        self.partitions = defaultdict(self.default_partition)
    
    def default_partition(self):
        return {'data': [], 'size': self.default_particion_size}
    
    def get_partition(self, partition_name):
        return self.partitions[partition_name]
    
    def get_partition_data(self, partition_name):
        return self.partitions[partition_name]['data']
    
    def set_partition(self, partition_name, data, size=None):
        if size is None:
            size = self.default_particion_size
            
        self.partitions[partition_name] = {'data': data, 'size': size}
        
    def add_to_partition(self, partition_name, value) -> None:

        partition = self.partitions[partition_name]
        if len(partition['data']) >= partition['size']:
            partition['data'].pop(0)
            
        partition['data'].append(value)
        
    def get_last_item_in_partition(self, partition_name):
        partition = self.partitions[partition_name]
        partition['data'][-1]