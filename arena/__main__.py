# -*- coding: utf-8 -*-


def main():
    from dotenv import load_dotenv
    load_dotenv(verbose=True)

    import os
    data = {
        "secret_key": os.getenv("SECRET_KEY"),
        "sample_uri": os.getenv("SAMPLE_URI")
    }
    print("Your authentication information should show up here properly:")
    print(f"secretkey:{data['secret_key']}, uri:{data['sample_uri']}")

    import arena.core.sample as Sample
    Sample.hello_mongo(data['sample_uri'])
