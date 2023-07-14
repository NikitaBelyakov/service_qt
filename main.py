from database import create_session,global_init, Client,Car,ClientCar,Order
global_init("database/serv.db")
session = create_session()
#new = Client(full_name="Беляков Сергей Александрович",phone="89024764367")
#new = ClientCar(client_id=1,car_id=1)
#session.add(new)
#session.commit()
cl = session.query(ClientCar).filter(ClientCar.client_id==2 and ClientCar.car_id==2).first()
print(cl)


