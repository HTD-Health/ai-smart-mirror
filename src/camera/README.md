# Camera module


## Testing

```bash
# run event bus
docker-compose up event-bus

# run camera module
python run.py --image_dir=`pwd`

# send event to make a picture
python src/utils/send_event.py 1 ''
```
