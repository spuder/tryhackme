rule TBFC_Simple_MZ_Detect
{
    meta:
        author = "spuder"
        description = "Match TBFC: followed by ASCII alphanumeric keyword"

    strings:
        $foobar = /TBFC:[A-Za-z0-9]+/

    condition:
        $foobar
}