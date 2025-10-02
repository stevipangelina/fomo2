import folium
import heapq
import webbrowser

# Data node (kecamatan/kelurahan di Bandung) dan koordinatnya
nodes = {
    "Cicendo": [-6.9025, 107.5956],
    "Sukajadi": [-6.8929, 107.5936],
    "Coblong": [-6.8782, 107.6161],
    "Lengkong": [-6.9301, 107.6284],
    "Cibiru": [-6.9135, 107.7221],
    "Ujung Berung": [-6.9147, 107.7048],
    "Antapani": [-6.9195, 107.6502],
    "Buah Batu": [-6.9503, 107.6268],
    "Cidadap": [-6.8615, 107.6063],
    "Neglasari": [-6.8800, 107.6368],  
}

# Hubungan antar node (edges) dan jarak (km)
edges = [
    ("Cicendo", "Sukajadi", 2),
    ("Cicendo", "Coblong", 4),
    ("Sukajadi", "Coblong", 2.5),
    ("Coblong", "Lengkong", 3),
    ("Coblong", "Cidadap", 3.5),
    ("Lengkong", "Antapani", 4),
    ("Antapani", "Cibiru", 6),
    ("Cibiru", "Ujung Berung", 2),
    ("Lengkong", "Buah Batu", 2.5),
    ("Buah Batu", "Antapani", 3),
    ("Cidadap", "Sukajadi", 3),
    ("Neglasari", "Coblong", 2), 
    ("Neglasari", "Lengkong", 2.5), 
]

# Tambahkan semua edges ke graf
graph = {node: [] for node in nodes.keys()}
for edge in edges:
    start, end, distance = edge
    graph[start].append((end, distance))
    graph[end].append((start, distance))

# Fungsi Dijkstra untuk menemukan rute tercepat
def dijkstra(graph, start, end):
    queue = [(0, start, [])]
    visited = set()
    while queue:
        cost, node, path = heapq.heappop(queue)
        if node in visited:
            continue
        path = path + [node]
        visited.add(node)
        if node == end:
            return cost, path
        for neighbor, distance in graph[node]:
            if neighbor not in visited:
                heapq.heappush(queue, (cost + distance, neighbor, path))
    return float("inf"), []

# Fungsi untuk membuat peta dengan rute tercepat
def buat_peta(start, end):
    if start not in nodes or end not in nodes:
        print("Node tidak valid.")
        return

    # Temukan rute tercepat
    total_distance, shortest_path = dijkstra(graph, start, end)

    if total_distance == float("inf"):
        print("Tidak ada rute antara node awal dan akhir.")
        return

    # Peta pusat
    peta = folium.Map(location=[-6.9147, 107.6098], zoom_start=12)

    # Tambahkan penanda node ke peta
    for kecamatan, koordinat in nodes.items():
        folium.Marker(location=koordinat, popup=kecamatan, icon=folium.Icon(color="blue")).add_to(peta)

    # Tambahkan edges (garis dengan jarak) ke peta
    for edge in edges:
        start_node, end_node, distance = edge
        color = "gray"
        if (start_node in shortest_path and end_node in shortest_path) and (
            shortest_path.index(start_node) - shortest_path.index(end_node) in [-1, 1]
        ):
            color = "red"
        folium.PolyLine(
            locations=[nodes[start_node], nodes[end_node]],
            color=color,
            weight=3.5 if color == "red" else 2.5,
            opacity=0.8,
        ).add_to(peta)

        # Tambahkan label jarak di tengah garis
        midpoint = [
            (nodes[start_node][0] + nodes[end_node][0]) / 2,
            (nodes[start_node][1] + nodes[end_node][1]) / 2,
        ]
        folium.Marker(
            location=midpoint,
            icon=folium.DivIcon(html=f"<div style='font-size: 12px; color: black;'>{distance} km</div>"),
        ).add_to(peta)

    # Menghitung derajat setiap node dan mencari node dengan derajat tertinggi
    node_degrees = {node: len(graph[node]) for node in graph}
    max_degree_node = max(node_degrees, key=node_degrees.get)

    # Simpan peta ke file HTML
    file_name = "map_bandung.html"
    peta.save(file_name)

    # Tampilkan hasil kepada pengguna
    print(f"\nRute Maps Bandung tercepat disimpan di '{file_name}'.")
    print("\nStatistik Graf:")
    print(f"Rute: {' -> '.join(shortest_path)}")
    print(f"Jarak: {total_distance} km")
    print(f"Jumlah Node: {len(nodes)}")
    print(f"Jumlah Edge: {len(edges)}")
    print(f"\nNode dengan derajat tertinggi: {max_degree_node} -> Derajat: {node_degrees[max_degree_node]}")
    print("\nDaftar Node:")
    for node in nodes:
        print(f"- {node}")
    print("\nDaftar Edge:")
    for edge in edges:
        print(f"- {edge[0]} <-> {edge[1]} (Jarak: {edge[2]} km)")

    webbrowser.open(file_name)

# Program utama
def main():
    print("Daftar Node:")
    for node in nodes.keys():
        print(f"- {node}")

    start = input("Masukkan nama lokasi awal: ").strip().title()
    end = input("Masukkan nama lokasi akhir: ").strip().title()

    # Periksa jika node awal dan akhir valid
    if start not in nodes or end not in nodes:
        print("Nama node yang dimasukkan tidak valid.")
        return
    if start == end:
        print("Node awal dan akhir tidak boleh sama.")
    else:
        buat_peta(start, end)

# Jalankan program utama
if __name__ == "__main__":
    main()