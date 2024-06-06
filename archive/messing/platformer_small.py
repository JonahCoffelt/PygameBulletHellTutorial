from pygame import*;w=display.set_mode([800]*2);d=display;e=event;x,y,v,g=400,400,0,0
while not e.get(256):
    e.clear();w.fill(0);draw.rect(w,-1,(x,y,60,90));d.flip();k=key.get_pressed();v+=3e-4;y-=v*(g-1);g=y>710;x=min(max(x+.2*(k[100]-k[97]),0),740)
    if g&k[32]:v=-.4;g=0