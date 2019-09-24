using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ShotController : MonoBehaviour
{
    public float spd;

    Rigidbody rb;

    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody>();
        rb.velocity = transform.forward * spd;
    }

    

    // Update is called once per frame
    void Update()
    {
        rb.velocity = rb.velocity.normalized * spd;
    }
}
