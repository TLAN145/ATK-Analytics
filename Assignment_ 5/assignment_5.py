import open3d as o3d
import numpy as np
import copy
from pathlib import Path

# ========================================
# CONFIGURATION: Set the model path here
# ========================================
MODEL_PATH = Path(r"C:\Assignment_ 5\model2.obj")


def print_separator(step_number, step_name):
    print("\n" + "="*80)
    print(f"  STEP {step_number}: {step_name}")
    print("="*80)


def print_mesh_info(mesh, step_name="Mesh"):
    print(f"\n{step_name}:")
    print(f"  Number of vertices: {len(mesh.vertices)}")
    print(f"  Number of triangles: {len(mesh.triangles)}")
    print(f"  Has vertex colors: {'Yes' if mesh.has_vertex_colors() else 'No'}")
    print(f"  Has vertex normals: {'Yes' if mesh.has_vertex_normals() else 'No'}")


def print_pointcloud_info(pcd, step_name="Point Cloud"):
    print(f"\n{step_name}:")
    print(f"  Number of points: {len(pcd.points)}")
    print(f"  Has colors: {'Yes' if pcd.has_colors() else 'No'}")
    print(f"  Has normals: {'Yes' if pcd.has_normals() else 'No'}")


def print_voxel_info(voxel_grid, step_name="Voxel Grid"):
    print(f"\n{step_name}:")
    voxels = voxel_grid.get_voxels()
    print(f"  Number of voxels: {len(voxels)}")
    print(f"  Voxel size: {voxel_grid.voxel_size}")


# ========================================
# STEP 1: Loading and Visualization
# ========================================
def step1_load_and_visualize():
    print_separator(1, "Loading and Visualization")

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"File not found:\n{MODEL_PATH}")

    ext = MODEL_PATH.suffix.lower()

    print(f"\nDetected file type: {ext}")

    if ext in [".ply", ".obj", ".stl", ".off", ".gltf", ".glb"]:
        mesh = o3d.io.read_triangle_mesh(str(MODEL_PATH))
    else:
        mesh = o3d.geometry.TriangleMesh()

    if len(mesh.triangles) == 0:
        print("\nModel seems to contain NO TRIANGLES. Trying to load as point cloud...")
        pcd_direct = o3d.io.read_point_cloud(str(MODEL_PATH))

        if len(pcd_direct.points) > 0:
            print("Creating mesh from point cloud...")
            pcd_direct.estimate_normals()
            mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
                pcd_direct, depth=8)
            mesh.compute_vertex_normals()
        else:
            raise RuntimeError(f"Could not load model. Unsupported or corrupted file:\n{MODEL_PATH}")
    else:
        if not mesh.has_vertex_normals():
            mesh.compute_vertex_normals()

    print("\nModel loaded successfully!")
    print_mesh_info(mesh, "Original Model")

    print("\n>>> Opening visualization window...")
    o3d.visualization.draw_geometries([mesh],
                                      window_name="Step 1: Original Model",
                                      width=1024, height=768)
    return mesh


# ========================================
# STEP 2: Conversion to Point Cloud
# ========================================
def step2_convert_to_pointcloud(mesh):
    print_separator(2, "Conversion to Point Cloud")

    pcd = mesh.sample_points_uniformly(number_of_points=10000)

    print("\nConverted to point cloud!")
    print_pointcloud_info(pcd, "Point Cloud")

    print("\n>>> Opening visualization window...")
    o3d.visualization.draw_geometries([pcd],
                                      window_name="Step 2: Point Cloud",
                                      width=1024, height=768)
    return pcd


# ========================================
# STEP 3: Surface Reconstruction
# ========================================
def step3_surface_reconstruction(pcd):
    print_separator(3, "Surface Reconstruction from Point Cloud")

    print("\nEstimating normals...")
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
        radius=0.1, max_nn=30))
    pcd.orient_normals_consistent_tangent_plane(k=15)

    print("Performing Poisson reconstruction...")
    mesh_recon, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=9)

    print("Removing artifacts...")
    vertices_to_remove = densities < np.quantile(densities, 0.05)
    mesh_recon.remove_vertices_by_mask(vertices_to_remove)

    bbox = pcd.get_axis_aligned_bounding_box()
    mesh_cropped = mesh_recon.crop(bbox)
    mesh_cropped.compute_vertex_normals()

    print_mesh_info(mesh_cropped, "Reconstructed Surface")

    print("\n>>> Opening visualization window...")
    o3d.visualization.draw_geometries([mesh_cropped],
                                      window_name="Step 3: Reconstructed Surface",
                                      width=1024, height=768)
    return mesh_cropped


# ========================================
# STEP 4: Voxelization
# ========================================
def step4_voxelization(pcd):
    print_separator(4, "Voxelization")

    voxel_size = 0.10
    print(f"\nCreating voxel grid with voxel size = {voxel_size}")

    voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size)
    print_voxel_info(voxel_grid, "Voxel Grid")

    print("\n>>> Opening visualization window...")
    o3d.visualization.draw_geometries([voxel_grid],
                                      window_name="Step 4: Voxelization",
                                      width=1024, height=768)
    return voxel_grid


# ========================================
# STEP 5: Adding a Plane
# ========================================
def step5_add_plane(pcd):
    print_separator(5, "Adding a Plane")

    center = pcd.get_center()
    extent = pcd.get_max_bound() - pcd.get_min_bound()

    plane_height = extent[1] * 1.5
    plane_depth = extent[2] * 1.5

    plane = o3d.geometry.TriangleMesh.create_box(
        width=0.002, height=plane_height, depth=plane_depth)

    plane_center = center.copy()
    plane.translate(plane_center - plane.get_center())
    plane.paint_uniform_color([1.0, 0.3, 0.0])
    plane.compute_vertex_normals()

    print(f"\nPlane created: 0.002 x {plane_height:.3f} x {plane_depth:.3f}")
    print(f"Position: {plane_center}")

    print("\n>>> Opening visualization window...")
    o3d.visualization.draw_geometries([pcd, plane],
                                      window_name="Step 5: Object with Plane",
                                      width=1024, height=768)
    return center


# ========================================
# STEP 6: Surface Clipping
# ========================================
def step6_surface_clipping(pcd, plane_center):
    print_separator(6, "Surface Clipping")

    points = np.asarray(pcd.points)
    plane_normal = np.array([1, 0, 0])
    distances = np.dot(points - plane_center, plane_normal)
    mask = distances < 0

    pcd_clipped = pcd.select_by_index(np.where(mask)[0])

    print_pointcloud_info(pcd_clipped, "Clipped Point Cloud")
    print(f"  Points removed: {len(pcd.points) - len(pcd_clipped.points)}")

    print("\n>>> Opening visualization window...")
    o3d.visualization.draw_geometries([pcd_clipped],
                                      window_name="Step 6: Clipped Point Cloud",
                                      width=1024, height=768)
    return pcd_clipped


# ========================================
# STEP 7: Color and Extremes
# ========================================
# ========================================
# STEP 7: Color and Extremes + Show Extremes as Voxels
# ========================================
def step7_color_and_extremes(pcd_clipped):
    print_separator(7, "Color and Extremes")

    points = np.asarray(pcd_clipped.points)
    axis = 2  # Z-axis
    min_value, max_value = points[:, axis].min(), points[:, axis].max()
    min_index = np.argmin(points[:, axis])
    max_index = np.argmax(points[:, axis])

    normalized = (points[:, axis] - min_value) / (max_value - min_value)

    # Color gradient (red → blue)
    colors = np.zeros((len(points), 3))
    colors[:, 0] = normalized        # red channel
    colors[:, 2] = 1 - normalized    # blue channel

    pcd_colored = copy.deepcopy(pcd_clipped)
    pcd_colored.colors = o3d.utility.Vector3dVector(colors)

    # Extract extreme points
    min_point = points[min_index]
    max_point = points[max_index]

    print(f"\nLowest point (Z-min):  {min_point}")
    print(f"Highest point (Z-max): {max_point}")

    # Create voxel cubes at extreme points
    voxel_cube_size = (pcd_clipped.get_max_bound() - pcd_clipped.get_min_bound()).max() * 0.04

    cube_min = o3d.geometry.TriangleMesh.create_box(voxel_cube_size,
                                                    voxel_cube_size,
                                                    voxel_cube_size)
    cube_min.translate(min_point - cube_min.get_center())
    cube_min.paint_uniform_color([0.0, 0.0, 1.0])   # Blue

    cube_max = o3d.geometry.TriangleMesh.create_box(voxel_cube_size,
                                                    voxel_cube_size,
                                                    voxel_cube_size)
    cube_max.translate(max_point - cube_max.get_center())
    cube_max.paint_uniform_color([1.0, 0.0, 0.0])   # Red

    # Display both cubes with colored cloud
    print("\n>>> Opening visualization window...")
    o3d.visualization.draw_geometries([pcd_colored, cube_min, cube_max],
                                      window_name="Step 7: Color Gradient + Extreme Voxels",
                                      width=1024, height=768)

    return pcd_colored



# ========================================
# MAIN
# ========================================
def main():
    print("\n" + "="*80)
    print("  ASSIGNMENT 5 - 3D VISUALIZATION WITH OPEN3D")
    print("="*80)
    print(f"\nModel path:\n{MODEL_PATH}")
    input("\nPress Enter to start...")

    mesh = step1_load_and_visualize()
    pcd = step2_convert_to_pointcloud(mesh)
    step3_surface_reconstruction(pcd)
    step4_voxelization(pcd)
    plane_center = step5_add_plane(pcd)
    pcd_clipped = step6_surface_clipping(pcd, plane_center)
    step7_color_and_extremes(pcd_clipped)

    print("\n" + "="*80)
    print("All steps completed successfully!")
    print("="*80)


if __name__ == "__main__":
    main()
