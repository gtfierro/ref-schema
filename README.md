# Ref Schema

Docs are [here](https://ref-schema.brickschema.org/)

## Extending Ref Schema

Here's a short description of how to add a new external reference to `ref schema`

1. Create a new file under `models/` to contain the statements; create a new ontology URI that extends
   the `ref` URI. The base `ref` URI is `https://brickschema.org/schema/Brick/ref#`, so if you were creating
   an extension for a new protocol, say `Modbus`, then you might choose a URI of  `https://brickschema.org/schema/Brick/ref/modbus#`
2. Ensure the new file contains an ontology declaration using that URI:

   ```ttl
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix ref: <https://brickschema.org/schema/Brick/ref#> .
    @prefix sh: <http://www.w3.org/ns/shacl#> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix owl: <http://www.w3.org/2002/07/owl#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    @prefix modbus: <https://brickschema.org/schema/Brick/ref/modbus#> .

    modbus: a owl:Ontology .
    ```
3. Inside the new file, define all of the `owl:ObjectProperty` and `owl:DatatypeProperty` properties
   that would exist on the external reference shape. For Modbus, one might have:
   - IP address (for Modbus/TCP)
   - data type (one of `coil`, `contact`, `register`, ...)
   - address offset

   These properties should be in the `ref:` namespace, but the property names should start with
   some indication of the protocol (e.g. `modbus*`). You should have an `skos:definitions` and `rdfs:label`
   on each of these. You can use SHACL Property Shapes to further refine these definitions as well; (see step 5)

    ```ttl
    # continuation of above .ttl file
    ref:modbusIPAddress a owl:DatatypeProperty
        rdfs:label "Modbus IP address" ;
        skos:definition "IP address of Modbus TCP/IP server where the item exists" .
    ref:modbusDataType a owl:DatatypeProperty ;
        rdfs:label "Modbus data type" ;
        skos:definition "Data type of the modbus item being referenced" .
    ref:modbusAddressOffset a owl:DatatypeProperty ;
        rdfs:label "Modbus address offset" ;
        skos:definition "Offset into the modbus address space where the referenced item exists" .
    ```
4. Define a `<EXTERNAL REFERENCE>ReferenceShape` Node Shape in this new file which performs reflection on the reference
   in order to add the correct type annotation. This will refer to the `ref:<EXTERNAL REFERENCE>Reference` shape
   that we will define below. Here is an example of what this would look like for our Modbus shape:

   ```ttl
    ref:ModbusReferenceShape a sh:NodeShape ;
        skos:definition "Infers a ModbusReference instance from the object of an hasExternalReference." ;
        sh:targetObjectsOf ref:hasExternalReference ;
        sh:rule [
          a sh:TripleRule ;
          sh:condition ref:ModbusReference ;
          sh:subject sh:this ;
          sh:predicate rdf:type ;
          sh:object ref:ModbusReference ;
        ] ;
    .
    ```
5. In `model/all.ttl`, add your new `Reference` shape. This should be both an `owl:Class` and `sh:NodeShape` and a subclass of `ref:ExternalReference`.
   Use all of the propery shapes you defined above; you can decide if they are optional or necessary. The `Reference` shape should exist in the `ref:` namespace.
   You should include a `skos:definition` and `rdfs:label`.
   For our Modbus example:

   ```ttl
   ref:ModbusReference a owl:Class, sh:NodeShape ;
       rdfs:subClassOf ref:ExternalReference ;
       rdfs:label "Modbus Reference" ;
       skos:definition "Refers to a modbus item over TCP/IP" ;
       sh:property [
        sh:path ref:modbusIPAddress ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:string ;
       ] ;
       sh:property [
        sh:path ref:modbusDataType ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:string ;
        sh:in ("coil", "contact", "register") .
       ] ;
       sh:property [
        sh:path ref:modbusAddressOffset ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:nonNegativeInteger ;
       ] ;
    .
    ```
6. Finally add an import to your graph in `model/all.ttl`:

    ```ttl
    <https://brickschema.org/schema/Brick/ref> a owl:Ontology ;
        dcterms:title "Ref Schema" ;
        dcterms:creator ( [ a sdo:Person ;
                    sdo:email "gtfierro@mines.edu" ;
                    sdo:name "Gabe Fierro" ] ) ;
        owl:imports <https://brickschema.org/schema/Brick/ref/core#> ;
        owl:imports <https://brickschema.org/schema/Brick/ref/bacnet#> ;
        owl:imports <https://brickschema.org/schema/Brick/ref/ifc#> ;
        owl:imports <https://brickschema.org/schema/Brick/ref/tsdb#> ;
        owl:imports <https://brickschema.org/schema/Brick/ref/modbus#> ; # <--- added!
    .
    ```
