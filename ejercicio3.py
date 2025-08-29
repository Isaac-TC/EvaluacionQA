from dataclasses import dataclass
from typing import List, Dict, Optional
from abc import ABC, abstractmethod
import csv, io
@dataclass
class Item:
    id: int
    nombre: str
    categoria: str
    precio: float
    stock: int = 0

class Inventario:
    def __init__(self):
        self.items: Dict[int, Item] = {}

    def agregar_item(self, item: Item):
        self.items[item.id] = item

    def eliminar_item(self, item_id: int):
        return self.items.pop(item_id)

    def actualizar_stock(self, item_id: int, nuevo_stock: int):
        viejo = self.items[item_id].stock
        self.items[item_id].stock = nuevo_stock
        return viejo

    def listar(self):
        return list(self.items.values())

class OperacionesAdmin:
    def __init__(self, inventario: Inventario):
        self.inv = inventario

    def cambiar_precio(self, item_id: int, nuevo_precio: float):
        viejo = self.inv.items[item_id].precio
        self.inv.items[item_id].precio = nuevo_precio
        return viejo

    def eliminar_item(self, item_id: int):
        return self.inv.eliminar_item(item_id)

class ProxyAdmin:
    def __init__(self, admin_ops: OperacionesAdmin, role: str):
        self.admin = admin_ops
        self.role = role

    def check(self):
        if self.role != "admin":
            raise PermissionError("Solo admin puede hacer esto")

    def cambiar_precio(self, item_id, nuevo_precio):
        self.check()
        return self.admin.cambiar_precio(item_id, nuevo_precio)

    def eliminar_item(self, item_id):
        self.check()
        return self.admin.eliminar_item(item_id)

class Command(ABC):
    @abstractmethod
    def execute(self): ...
    @abstractmethod
    def undo(self): ...

class CmdAgregar(Command):
    def __init__(self, inv: Inventario, item: Item):
        self.inv = inv
        self.item = item
    def execute(self):
        self.inv.agregar_item(self.item)
    def undo(self):
        self.inv.eliminar_item(self.item.id)

class CmdActualizarStock(Command):
    def __init__(self, inv: Inventario, item_id: int, nuevo: int):
        self.inv = inv
        self.item_id = item_id
        self.nuevo = nuevo
        self.viejo: Optional[int] = None
    def execute(self):
        self.viejo = self.inv.actualizar_stock(self.item_id, self.nuevo)
    def undo(self):
        if self.viejo is not None:
            self.inv.actualizar_stock(self.item_id, self.viejo)

class CmdCambiarPrecio(Command):
    def __init__(self, proxy: ProxyAdmin, item_id: int, nuevo: float):
        self.proxy = proxy
        self.item_id = item_id
        self.nuevo = nuevo
        self.viejo: Optional[float] = None
    def execute(self):
        self.viejo = self.proxy.cambiar_precio(self.item_id, self.nuevo)
    def undo(self):
        if self.viejo is not None:
            self.proxy.cambiar_precio(self.item_id, self.viejo)

class GestorComandos:
    def __init__(self):
        self.historial: List[Command] = []
    def ejecutar(self, cmd: Command):
        cmd.execute()
        self.historial.append(cmd)
    def deshacer(self):
        if self.historial:
            cmd = self.historial.pop()
            cmd.undo()

class ReportBuilder(ABC):
    @abstractmethod
    def build(self, items: List[Item]) -> str: ...

class CSVReportBuilder(ReportBuilder):
    def build(self, items: List[Item]) -> str:
        out = io.StringIO()
        writer = csv.writer(out)
        writer.writerow(["id","nombre","categoria","precio","stock"])
        for it in items:
            writer.writerow([it.id, it.nombre, it.categoria, it.precio, it.stock])
        return out.getvalue()

class MarkdownReportBuilder(ReportBuilder):
    def build(self, items: List[Item]) -> str:
        header = "| id | nombre | categoria | precio | stock |\n"
        sep = "|---|---|---|---|---|\n"
        body = ""
        for it in items:
            body += f"| {it.id} | {it.nombre} | {it.categoria} | {it.precio} | {it.stock} |\n"
        return header + sep + body

if __name__ == "__main__":
    inv = Inventario()
    admin_real = OperacionesAdmin(inv)
    admin = ProxyAdmin(admin_real, "admin")
    user = ProxyAdmin(admin_real, "user")

    gestor = GestorComandos()

    gestor.ejecutar(CmdAgregar(inv, Item(1,"Teclado","Perif",25,10)))
    gestor.ejecutar(CmdAgregar(inv, Item(2,"Mouse","Perif",15,5)))
    gestor.ejecutar(CmdAgregar(inv, Item(3,"Laptop","PCs",800,2)))

    print("Inventario inicial:", [i.__dict__ for i in inv.listar()])

    gestor.ejecutar(CmdCambiarPrecio(admin, 3, 750))
    print("Precio laptop cambiado:", inv.items[3].precio)

    
    gestor.ejecutar(CmdActualizarStock(inv, 2, 12))
    print("Stock mouse actualizado:", inv.items[2].stock)

  
    gestor.deshacer()
    print("Deshacer -> stock mouse:", inv.items[2].stock)

    rep_csv = CSVReportBuilder().build(inv.listar())
    print("\nReporte CSV:\n", rep_csv)

    rep_md = MarkdownReportBuilder().build(inv.listar())
    print("Reporte Markdown:\n", rep_md)
