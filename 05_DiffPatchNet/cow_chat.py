import asyncio
from cowsay import list_cows, cowsay

clients = {}
cow_set = set(list_cows())

async def cow_chat(reader, writer):
    is_active = False
    is_quit = False

    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(asyncio.Queue().get())

    while not reader.at_eof() and not is_quit:
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                input_line = q.result().decode().strip().split()
                if len(input_line) == 0:
                    continue
                command = input_line[0]

                if command == 'who':
                    writer.write(f"Active cows: \n{', '.join(clients.keys())}\n".encode())
                    await writer.drain()

                elif command == 'cows':
                    writer.write(f"Available cows: {', '.join(cow_set)}\n".encode())

                elif command == 'login':
                    if is_active:
                        writer.write(f"You already registered as {me}\n".encode())
                        await writer.drain()
                    else:
                        if len(input_line) < 2:
                            writer.write("No argument for login\n".encode())
                            await writer.drain()
                        else:
                            me = input_line[1]
                            if me in cow_set:
                                cow_set.remove(me)
                                clients[me] = asyncio.Queue()
                                is_active = True
                                print(f"{me} is here")

                                for out in clients.values():
                                    if out is not clients[me]:
                                        await out.put(f"{me} is here")
                                writer.write(f"Registered as {me}\n".encode())
                                await writer.drain()

                                receive.cancel()
                                receive = asyncio.create_task(clients[me].get())
                            else:
                                writer.write("That cow is unavailable\n".encode())
                                await writer.drain()
                
                elif command == 'say':
                    if not is_active:
                        writer.write("You have to login first\n".encode())
                        await writer.drain()
                    else:
                        if len(input_line) < 3:
                            writer.write("No arguments for say\n".encode())
                            await writer.drain()
                        else:
                            reciever = input_line[1]
                            message = ' '.join(input_line[2:])
                            await clients[reciever].put(f"{me} whispers:\n{cowsay(message, cow=me)}")
                            writer.write(f"{me} whispers:\n{cowsay(message, cow=me)}\n".encode())
                            await writer.drain()

                elif command == 'yield':
                    if not is_active:
                        writer.write("You have to login first\n".encode())
                        await writer.drain()
                    else:
                        if len(input_line) < 2:
                            writer.write("No argument for yield\n".encode())
                            await writer.drain()
                        else:
                            message = ' '.join(input_line[1:])
                            for out in clients.values():
                                if out is not clients[me]:
                                    await out.put(f"{me} says:\n{cowsay(message, cow=me)}")
                            writer.write(f"{me} says:\n{cowsay(message, cow=me)}\n".encode())
                            await writer.drain()

                elif command == 'quit':
                    for out in clients.values():
                        if out is not clients[me]:
                            await out.put(f"{me} leaves")

                    is_quit = True
                    break
                else:
                    continue
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()

    send.cancel()
    receive.cancel()

    print(f"{me} leaves")
    del clients[me]
    cow_set.add(me)
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(cow_chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
