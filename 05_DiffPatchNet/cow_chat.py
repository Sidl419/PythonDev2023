import asyncio
import shlex
import readline

from cowsay import list_cows

clients = {}
cow_set = set(list_cows())

async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = asyncio.Queue()
    is_active = False

    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())

    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                input_line = shlex.split(q.result().decode().strip())
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
                            name = input_line[1]
                            if name in cow_set:
                                cow_set -= set(name)
                                clients[name] = asyncio.Queue()
                                writer.write(f"Registered as {name}\n".encode())
                                await writer.drain()
                                is_active = True
                                receive.cancel()
                                receive = asyncio.create_task(clients[me].get())
                            else:
                                writer.write("That cow is unavailable\n".encode())
                                await writer.drain()
                else:
                    for out in clients.values():
                        if out is not clients[me]:
                            await out.put(f"{me} {q.result().decode().strip()}")
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
