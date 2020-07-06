from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = "STORAGE_ACCOUNT_NAME"
    account_key = "ACCOUNT_KEY"
    azure_container = 'media'
    file_overwrite = True
    expiration_secs = None
    

class AzureStaticStorage(AzureStorage):
    account_name = "STORAGE_ACCOUNT_NAME"
    account_key = "ACCOUNT_KEY"
    azure_container = 'static'
    expiration_secs = None