import asyncio
import json 
import jsonlines
import os
from pathlib import Path
from typing import Any

from config.settings import DATA_DIR

__all__ = ['JSONHandler', 'JSONLineHandler']


class JSONHandler:

    filename: str
    filepath: Path
    lock: asyncio.Lock
    loop: asyncio.AbstractEventLoop
    default_data: dict

    def __init__(self, filename: str, *args, default_data: dict = None, **kwargs):
        self.filename = DATA_DIR / filename
        self.filepath = Path(self.filename)
        self.lock = asyncio.Lock()
        self.loop = kwargs.pop('loop', asyncio.get_running_loop())
        self.default_data = default_data or {}
        if not self.filepath.exists():
            self.filepath.touch()
            self.s_clear()

    def s_read(self) -> Any:
        with self.filepath.open('r', encoding='utf-8') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}

    def s_write(self, data: Any) -> None:
        with self.filepath.open('w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def s_get(self, key: str) -> Any:
        data = self.s_read()
        return data.get(key)

    def s_update(self, key: str, value: Any) -> None:
        data = self.s_read()
        data[key] = value
        self.s_write(data)

    def s_remove(self, key: str) -> None:
        data = self.s_read()
        if key in data:
            del data[key]
            self.s_write(data)

    def s_clear(self) -> None:
        self.s_write(self.default_data)

    async def read(self) -> Any:
        async with self.lock:
            return await self.loop.run_in_executor(None, self.s_read)

    async def write(self, data: Any) -> None:
        async with self.lock:
            await self.loop.run_in_executor(None, self.s_write, data)

    async def get(self, key: str) -> Any:
        async with self.lock:
            return await self.loop.run_in_executor(None, self.s_get, key)

    async def update(self, key: str, value: Any) -> None:
        async with self.lock:
            await self.loop.run_in_executor(None, self.s_update, key, value)

    async def remove(self, key: str) -> None:
        async with self.lock:
            await self.loop.run_in_executor(None, self.s_remove, key)

    async def clear(self) -> None:
        async with self.lock:
            await self.loop.run_in_executor(None, self.s_clear)


class JSONLineHandler:

    filename: str
    filepath: Path
    key_name: str
    lock: asyncio.Lock
    loop: asyncio.AbstractEventLoop
    unique_only: bool

    def __init__(self, filename: str, key_name: str, *args, default_data: Any = None, unique_only: bool = False, **kwargs):
        self.filename = DATA_DIR / filename
        self.filepath = Path(self.filename)
        self.key_name = key_name
        self.lock     = asyncio.Lock()
        self.loop     = kwargs.pop('loop', asyncio.get_running_loop())
        self.unique_only = unique_only
        self._ensure_exists()
        
    def _ensure_exists(self):
        if not self.filepath.parent.exists():
            self.filepath.parent.mkdir(parents=True)
        if not self.filepath.exists():
            self.filepath.touch()
            


    def s_get(self, key: Any = None, value: Any = None) -> dict:
        if value is None:
            raise ValueError('Value cannot be None')
        key = key or self.key_name
        with jsonlines.open(self.filename, 'r') as reader:
            for line in reader:
                if line[key] == value:
                    return line

    def s_get_all(self, key: Any = None, value: Any = None) -> list:
        if value is None:
            raise ValueError('Value cannot be None')
        key = key or self.key_name
        with jsonlines.open(self.filename, 'r') as reader:
            return [line for line in reader if line[key] == value]
    
    def s_read(self) -> list:
        with jsonlines.open(self.filename, 'r') as reader:
            return list(reader)
    
    def s_add(self, data: dict) -> None:
        with jsonlines.open(self.filename, 'a') as writer:
            if self.unique_only:
                if self.s_get(self.key_name, data[self.key_name]):
                    return
            writer.write(data)

    def s_update(self, key: Any = None, value: Any = None, data: dict = None) -> None:
        if value is None:
            raise ValueError('Value cannot be None')
        key = key or self.key_name
        temp_filepath = self.filepath.with_suffix('.tmp')
        updated = False
        with jsonlines.open(self.filename, 'r') as reader, jsonlines.open(temp_filepath, 'w') as writer:
            for line in reader:
                if line[key] == value and not updated:
                    writer.write(data)
                    updated = True
                else:
                    writer.write(line)
        if updated:
            os.replace(temp_filepath, self.filename)
        else:
            os.remove(temp_filepath)
            self.s_add(data)
        
    def s_remove(self, key: Any = None, value: Any = None) -> None:
        if value is None:
            raise ValueError('Value cannot be None')
        key = key or self.key_name
        temp_filepath = self.filepath.with_suffix('.tmp')
        with jsonlines.open(self.filename, 'r') as reader, jsonlines.open(temp_filepath, 'w') as writer:
            for line in reader:
                if line[key] != value:
                    writer.write(line)
        os.replace(temp_filepath, self.filename)

    def s_clear(self) -> None:
        self.filepath.unlink()
        self.filepath.touch()
    
    async def get(self, key: Any = None, value: Any = None) -> dict:
        async with self.lock:
            return await self.loop.run_in_executor(None, self.s_get, key, value)
    
    async def get_all(self, key: Any = None, value: Any = None) -> list:
        async with self.lock:
            return await self.loop.run_in_executor(None, self.s_get_all, key, value)

    async def read(self) -> list:
        async with self.lock:
            return await self.loop.run_in_executor(None, self.s_read)
        
    async def add(self, data: dict) -> None:
        async with self.lock:
            await self.loop.run_in_executor(None, self.s_add, data)

    async def update(self, key: Any = None, value: Any = None, data: dict = None) -> None:
        async with self.lock:
            await self.loop.run_in_executor(None, self.s_update, key, value, data)
    
    async def remove(self, key: Any = None, value: Any = None) -> None:
        async with self.lock:
            await self.loop.run_in_executor(None, self.s_remove, key, value)
    
    async def clear(self) -> None:
        async with self.lock:
            await self.loop.run_in_executor(None, self.s_clear)
    
    