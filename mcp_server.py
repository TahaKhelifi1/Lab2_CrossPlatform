import sys
from pathlib import Path
from typing import List

# Add project path so imports from main work when running inside containers
sys.path.append(str(Path(__file__).parent))

try:
    from fastmcp import FastMCP
except Exception:
    FastMCP = None

from main import SessionLocal, Product

# ---------------------- MCP SERVER ----------------------
if FastMCP is not None:
    mcp = FastMCP(name="Product Catalog MCP Server")


    @mcp.tool()
    def list_products() -> List[dict]:
        """Liste tous les produits du catalogue"""
        with SessionLocal() as db:
            products = db.query(Product).all()
            result = [{"id": p.id, "name": p.name, "price": p.price} for p in products]
            return result


    @mcp.tool()
    def get_product(product_id: int) -> dict:
        """Retourne un produit sp\u00e9cifique par son ID"""
        with SessionLocal() as db:
            product = db.query(Product).filter(Product.id == product_id).first()
            if product:
                return {"id": product.id, "name": product.name, "price": product.price}
            return {"error": "Product not found"}


    if __name__ == "__main__":
        mcp.run()
else:
    # Provide a simple CLI fallback so the module doesn't completely fail if fastmcp is missing.
    def _list_products_cli():
        with SessionLocal() as db:
            products = db.query(Product).all()
            for p in products:
                print(f"{p.id}: {p.name} - {p.price}")

    if __name__ == "__main__":
        print("fastmcp is not installed; running CLI fallback to list products\n")
        _list_products_cli()
