import socket
import os
import cv2
import pickle,struct
class server:
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ip=socket.gethostbyname(socket.gethostname())
    port=60000
    s.bind((ip,port))
    s.listen(10)
    print("server is running on ",ip)
    print("server port number",port)

    while True:
        client,adr=s.accept()
        print(adr)

        def inputcommand(client,adr):
           def sendfilefromserver(client,adr):
               print("here you can send file to client")
               file_name=client.recv(1024).decode()
               if not os.path.exists(file_name):
                  client.send("file-does not exits".encode())
               else:
                  client.send("file-exits".encode())
                  print("Sending",file_name)
                  if data !="":
                     file=open(file_name,'rb')
                     data=file.read(1024)
                     while data:
                        client.send(data)
                        data=file.read(1024)
                     client.shutdown(socket.SHUT_RDWR)
                     client.close()

           def recivefilefromclient(client,adr):
              file_name=input("enter file name")
              client.send(file_name.encode())

              confirmation=client.recv(1024)

              if confirmation.decode()=="file-does not exist":
                  print("file is not exist on that path")

              else:
                  write_name=file_name
                  if os.path.exists(write_name): os.remove(write_name)
                  with open(write_name,'wb') as file:
                      while 1:
                          data=client.recv(1024)
                          if not data:
                              break
                          file.write(data)
                  print(file_name,"successfully download")

              client.close()
           def commandfun(client,adr):
               command=input("enter command for client").encode()
               client.send(command)
               output=client.recv(1024).encode()
               print(output)
           def clientscren(client,adr):
               data=b""
               payload_size=struct.calcsize("Q")
               while len(data)<payload_size:
                   packet=client.recv(4*1024)
                   if not packet:break
                   data+=packet
               packed_msg_size=data[:payload_size]
               data=data[payload_size:]
               msg_size=struct.unpack("Q",packed_msg_size)[0]
               while len(data)<msg_size:
                   data+=client.recv(4*1024)
               frame_data=data[:msg_size]
               data=data[msg_size:]
               frame=pickle.loads(frame_data)
               img=cv2.cvtColor(np.float32(frame),cv2.COLOR_RGB2BGR)
               img=cv2.imshow("client screen",img)
               key=cv2.waitKey(1) & 0xFF
               if key==ord('q'):
                  pass
               client.close()
          
           input_command=input("command")
           if input_command=="sendfilefromserver":
              client.send("recivefile".encode())
              if __name__=="__main__":
                 sendfilefromserver(client,adr)
           elif input_command=="recivefilefromclient":
              client.send("sendfile".encode())
              if __name__=="__main__":
                 recivefilefromclient(client,adr)
           elif input_command=="send command":
              client.send("commandfun".encode())
              if __name__=="__main__":
                  commandfun(client,adr)
           elif input_command=="client screen":
               client.send("clientscren".encode())
               clientscreen(client,adr)
           else:
               print("wrong input")

           
        if __name__=="__main__":

            inputcommand(client,adr)


server=server()
