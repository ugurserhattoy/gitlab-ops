### gitlab-ops-cli

### Requirements
1. gitlab private token with api permissions
2. docker
### Installation 
1. Update .env file's BASE to your gitlab-ops-api endpoint
2. Make install.sh executable
```sh
chmod +x install.sh
```
3. Run install.sh
```sh
# for macOS
./install.sh mac 
# for linux
./install.sh linux
```
### Usage
To run gitlab ops anytime:
```sh
gitlab-ops
```
First you need to create a user in the login screen If you didn't already.
