using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;


[System.Serializable]
public class LevelCreator : MonoBehaviour
{
    Dictionary<Vector2Int, GameObject> walls = new Dictionary<Vector2Int, GameObject>();
    public Camera cam;
    public GameObject wall;
    public bool WallsAround = true;

    public GameObject wallPlacementIndicator;

    public uint xres, yres;
    Vector2Int gridSelection;
    

    float wallScaleY {get {
            return 0.5f * transform.localScale.z / (float)yres;
        } 
    }
    float wallScaleX {get {
            return 0.5f * transform.localScale.x / (float)xres;
        } 
    }

    // Start is called before the first frame update
    void Start()
    {
        if (WallsAround) {
            for(int i = 0; i < xres; i++)
            for(int j = 0; j < yres; j++) {
                if (i * j * (yres - 1 - j) * (xres - 1 - i) == 0) {
                    PlaceWall(new Vector2Int(i, j));
                }
            }
        }
    }
    void Awake() {
        
    }

    // Update is called once per frame
    void Update()
    {
        wallPlacementIndicator.transform.localScale = new Vector3(2.0f * wallScaleX, wallScaleX + wallScaleY, 2.0f * wallScaleY);
        //if (Input.GetMouseButtonDown(0))
        //    PlaceWall();
        ShowWallPlacement();

    }
    

    void OnMouseDown() {
        if (wallPlacementIndicator.activeInHierarchy) {
            PlaceWall();

        }
    }

    void PlaceWall(Vector2Int gridPos) {

        GameObject wallInstance = Instantiate(wall, GetPositionOfGrid(gridPos), Quaternion.identity);
        wallInstance.transform.localScale = wallPlacementIndicator.transform.localScale;
        wallInstance.transform.parent = transform;
        walls[gridSelection] = wallInstance;
        wallInstance.GetComponent<WallController>().LevelPos = gridSelection;
        wallPlacementIndicator.SetActive(false);
    }

    void PlaceWall() {
        GameObject wallInstance = Instantiate(wall, wallPlacementIndicator.transform.position, Quaternion.identity);
        wallInstance.transform.localScale = wallPlacementIndicator.transform.localScale;
        wallInstance.transform.parent = transform;
        walls[gridSelection] = wallInstance;
        wallInstance.GetComponent<WallController>().LevelPos = gridSelection;
        wallPlacementIndicator.SetActive(false);
    }

    Vector2Int GetGridSelection(RaycastHit hit) {
        int xCoord = (int) ((float) xres * (transform.localScale.x * 0.5f - (hit.point.x - transform.position.x)) / transform.localScale.x);
        int yCoord = (int) ((float) yres * (transform.localScale.z * 0.5f - (hit.point.z - transform.position.z)) / transform.localScale.z);
        return new Vector2Int(xCoord, yCoord);
    }

    Vector3 GetPositionOfGrid(Vector2Int gridSelection) {
        return new Vector3(transform.position.x + transform.localScale.x * 0.5f - 2.0f * (float)gridSelection.x * wallScaleX - wallScaleX, 
                transform.localScale.y*0.5f + wallPlacementIndicator.transform.localScale.y*0.5f, 
                transform.position.z + transform.localScale.z * 0.5f - 2.0f * (float)gridSelection.y * wallScaleY - wallScaleY);
    }

    public void RemoveWall(Vector2Int pos) {
        if (!walls.ContainsKey(pos))
            return;

        
        Object.Destroy(walls[pos]);
        walls.Remove(pos);

    }

    bool ShowWallPlacement() {
        Ray ray = cam.ScreenPointToRay(Input.mousePosition);
        RaycastHit hit;
        
        if (Physics.Raycast(ray, out hit)) {
            wallPlacementIndicator.SetActive(true);
            if (hit.transform != transform) {
                wallPlacementIndicator.SetActive(false);
                return false;
            }
            gridSelection = GetGridSelection(hit);
            
            wallPlacementIndicator.transform.position = GetPositionOfGrid(gridSelection);
            
            return true;
        }
        return false;
    }
}
