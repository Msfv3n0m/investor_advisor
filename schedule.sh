if ! command -v docker &> /dev/null
then
    echo "docker not installed/on path"
    exit 1
fi
crontab -l > mycron
echo "30 9 * * * cd $(pwd) && docker compose up -d" >> mycron
crontab mycron
rm mycron
