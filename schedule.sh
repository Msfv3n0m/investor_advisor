if ! command -v docker &> /dev/null
then
    echo "docker not installed/on path"
    exit 1
fi
crontab -l > mycron
echo "0 10 * * * cd $(pwd) && docker compose up -d" >> mycron
sudo crontab mycron
rm mycron
