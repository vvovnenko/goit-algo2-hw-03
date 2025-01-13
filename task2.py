import csv
import timeit
from typing import List, Dict, Any, Tuple
from BTrees.OOBTree import OOBTree


def add_item_to_tree(tree: OOBTree, item: Dict[str, Any]) -> None:
    """Додає елемент до OOBTree."""

    tree[item["ID"]] = item


def add_item_to_dict(
    data_dict: Dict[int, Dict[str, Any]], item: Dict[str, Any]
) -> None:
    """Додає елемент до словника."""

    data_dict[item["ID"]] = item


def range_query_tree(
    tree: OOBTree, min_price: float, max_price: float
) -> List[Dict[str, Any]]:
    """Виконує запит на діапазон цін у OOBTree."""

    return [item for _, item in tree.items(min_price, max_price)]


def range_query_dict(
    data_dict: Dict[int, Dict[str, Any]], min_price: float, max_price: float
) -> List[Dict[str, Any]]:
    """Виконує запит на діапазон цін у словнику."""

    return [
        item for item in data_dict.values() if min_price <= item["Price"] <= max_price
    ]


def load_items_from_csv(
    file_path: str, tree: OOBTree, data_dict: Dict[int, Dict[str, Any]]
) -> None:
    """Завантажує дані з CSV-файлу в OOBTree та словник."""

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            item = {
                "ID": int(row["ID"]),
                "Name": row["Name"],
                "Category": row["Category"],
                "Price": float(row["Price"]),
            }
            add_item_to_tree(tree, item)
            add_item_to_dict(data_dict, item)


def compare_query_performance(
    btree: OOBTree,
    data_dict: Dict[int, Dict[str, Any]],
    min_price: float,
    max_price: float,
    execution_number: int = 100,
) -> None:
    """Вимірює та виводить час виконання запитів на діапазон цін для OOBTree та словника."""

    tree_time: float = timeit.timeit(
        lambda: range_query_tree(btree, min_price, max_price), number=execution_number
    )
    print(f"Час виконання запиту на діапазон цін для OOBTree: {tree_time:.6f} секунд")

    dict_time: float = timeit.timeit(
        lambda: range_query_dict(data_dict, min_price, max_price),
        number=execution_number,
    )
    print(f"Час виконання запиту на діапазон цін для словника: {dict_time:.6f} секунд")


def main() -> None:
    """Головна функція програми."""

    btree: OOBTree = OOBTree()
    data_dict: Dict[int, Dict[str, Any]] = {}

    load_items_from_csv("generated_items_data.csv", btree, data_dict)

    compare_query_performance(btree, data_dict, 55, 250)


if __name__ == "__main__":
    main()
