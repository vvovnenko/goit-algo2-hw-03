import networkx as nx
from typing import Dict, List, Tuple, Any


def initialize_logistics_graph(edges: List[Tuple[str, str, int]]) -> nx.DiGraph:
    """Ініціалізує направлений граф, що представляє систему логістики."""
    graph = nx.DiGraph()

    for start_node, end_node, capacity in edges:
        graph.add_edge(start_node, end_node, capacity=capacity)

    return graph


def get_exit_points(graph: nx.DiGraph) -> List[str]:
    """Знаходить всі вузли у графі, які не мають вихідних ребер."""
    return [node for node, out_degree in graph.out_degree() if out_degree == 0]


def get_entry_points(graph: nx.DiGraph) -> List[str]:
    """Знаходить всі вузли у графі, які не мають вхідних ребер."""
    return [node for node, in_degree in graph.in_degree() if in_degree == 0]


def get_intermediates(graph: nx.DiGraph) -> List[str]:
    """Знаходить всі вузли у графі, які мають і вхідні, і вихідні ребра."""
    return [
        node
        for node in graph.nodes
        if graph.in_degree(node) > 0 and graph.out_degree(node) > 0
    ]


def compute_max_flow(
    graph: nx.DiGraph, entry_points: List[str], exit_points: List[str]
) -> Tuple[int, Dict[str, Dict[str, int]]]:
    """Обчислює максимальний потік між вхідними і вихідними точками."""
    source = "Вхід"
    sink = "Вихід"

    for entry in entry_points:
        graph.add_edge(source, entry, capacity=float("inf"))

    for exit_point in exit_points:
        graph.add_edge(exit_point, sink, capacity=float("inf"))

    flow_value, flow_details = nx.maximum_flow(
        graph, source, sink, flow_func=nx.algorithms.flow.edmonds_karp
    )

    graph.remove_node(source)
    graph.remove_node(sink)

    return flow_value, flow_details


def correlate_flows(
    flow_details: Dict[str, Dict[str, int]],
    entries: List[str],
    intermediates: List[str],
    exits: List[str],
) -> Dict[Tuple[str, str], int]:
    """Відображає потоки від вхідних точок до вихідних через проміжні."""
    flow_mapping: Dict[Tuple[str, str], int] = {}

    for entry, exit_point in [(e, x) for e in entries for x in exits]:
        total_flow = sum(
            min(
                flow_details.get(entry, {}).get(intermediate, 0),
                flow_details.get(intermediate, {}).get(exit_point, 0),
            )
            for intermediate in intermediates
        )
        flow_mapping[(entry, exit_point)] = total_flow

    return flow_mapping


def setup_graph(
    connections: List[Tuple[str, str, int]]
) -> Tuple[nx.DiGraph, List[str], List[str], List[str]]:
    """Налаштовує логістичний граф та отримує ключові точки."""
    graph = initialize_logistics_graph(connections)
    entry_points = get_entry_points(graph)
    intermediates = get_intermediates(graph)
    exit_points = get_exit_points(graph)
    return graph, entry_points, intermediates, exit_points


def display_flow(flow_details: Dict[str, Dict[str, int]]) -> None:
    """Виводить розподіл потоку в мережі."""
    print("Розподіл потоків:")
    for start, targets in flow_details.items():
        for end, flow in targets.items():
            if flow > 0:
                print(f"  {start} -> {end}: {flow}")


def display_mapping(flow_mapping: Dict[Tuple[str, str], int]) -> None:
    """Виводить карту потоків від терміналів до магазинів."""
    print("\nКарта потоків від терміналів до магазинів:")
    print("| Термінал   | Магазин    | Потік   |")
    print("| ---------- | ---------- | ------- |")
    for (entry, exit_point), flow in flow_mapping.items():
        print(f"| {entry:<10} | {exit_point:<10} | {flow:<7} |")


def main() -> None:
    edges = [
        ("Термінал 1", "Склад 1", 25),
        ("Термінал 1", "Склад 2", 20),
        ("Термінал 1", "Склад 3", 15),
        ("Термінал 2", "Склад 3", 15),
        ("Термінал 2", "Склад 4", 30),
        ("Термінал 2", "Склад 2", 10),
        ("Склад 1", "Магазин 1", 15),
        ("Склад 1", "Магазин 2", 10),
        ("Склад 1", "Магазин 3", 20),
        ("Склад 2", "Магазин 4", 15),
        ("Склад 2", "Магазин 5", 10),
        ("Склад 2", "Магазин 6", 25),
        ("Склад 3", "Магазин 7", 20),
        ("Склад 3", "Магазин 8", 15),
        ("Склад 3", "Магазин 9", 10),
        ("Склад 4", "Магазин 10", 20),
        ("Склад 4", "Магазин 11", 10),
        ("Склад 4", "Магазин 12", 15),
        ("Склад 4", "Магазин 13", 5),
        ("Склад 4", "Магазин 14", 10),
    ]

    logistics_graph, entry_points, intermediates, exit_points = setup_graph(edges)

    max_flow, flow_details = compute_max_flow(
        logistics_graph, entry_points, exit_points
    )
    print(f"Максимальний потік у мережі: {max_flow}")

    display_flow(flow_details)

    flow_mapping = correlate_flows(
        flow_details, entry_points, intermediates, exit_points
    )
    display_mapping(flow_mapping)


if __name__ == "__main__":
    main()
