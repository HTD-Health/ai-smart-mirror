# Camera module

## TODO:
https://www.losant.com/blog/how-to-access-the-raspberry-pi-camera-in-docker

## Testing

```bash
# run event bus
docker-compose up event-bus

# run camera module
python run.py --image_dir=`pwd`

# send event to make a picture
python src/utils/send_event.py 1 ''
```
