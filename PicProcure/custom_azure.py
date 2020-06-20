from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'demoblobstorage101' # Must be replaced by your <storage_account_name>
    account_key = 'rnT6wujj8Pmh6P1HjtH6p3KfRr6deJcWLwgFgoIpGKYzSk+EOHt+bfIE4ixtIB40yfhc10aLAKKYy91h1xS+4A==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'demoblobstorage101' # Must be replaced by your storage_account_name
    account_key = 'rnT6wujj8Pmh6P1HjtH6p3KfRr6deJcWLwgFgoIpGKYzSk+EOHt+bfIE4ixtIB40yfhc10aLAKKYy91h1xS+4A==' # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None