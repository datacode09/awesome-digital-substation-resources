<?xml version="1.0" encoding="UTF-8"?>
<!-- Tiny teaching SCD: one feeder protection IED and one merging unit. -->
<SCL xmlns="http://www.iec.ch/61850/2003/SCL" version="2007" revision="B">
  <Header id="demo" version="1"/>
  <Substation name="S1">
    <VoltageLevel name="E1">
      <Bay name="Q1">
        <ConductingEquipment name="CB1" type="CBR"/>
        <ConductingEquipment name="CT1" type="CTR"/>
      </Bay>
    </VoltageLevel>
  </Substation>
  <Communication>
    <SubNetwork name="ProcessBus" type="8-MMS">
      <ConnectedAP iedName="PROT1" apName="P1">
        <Address><P type="IP">10.0.0.11</P></Address>
        <GSE ldInst="LD0" cbName="gcb1">
          <Address><P type="MAC-Address">01-0C-CD-01-00-01</P><P type="APPID">0001</P><P type="VLAN-ID">000</P><P type="VLAN-PRIORITY">4</P></Address>
          <MinTime>4</MinTime><MaxTime>1000</MaxTime>
        </GSE>
      </ConnectedAP>
      <ConnectedAP iedName="MU1" apName="P1">
        <Address><P type="IP">10.0.0.21</P></Address>
        <SMV ldInst="LD0" cbName="msvcb1">
          <Address><P type="MAC-Address">01-0C-CD-04-00-01</P><P type="APPID">4000</P></Address>
        </SMV>
      </ConnectedAP>
    </SubNetwork>
  </Communication>
  <IED name="PROT1">
    <AccessPoint name="P1"><Server><LDevice inst="LD0">
      <LN0 lnClass="LLN0" inst="" lnType="LLN0t">
        <DataSet name="gooseDs"><FCDA ldInst="LD0" prefix="" lnClass="PTRC" lnInst="1" doName="Tr" daName="general" fc="ST"/>
                                <FCDA ldInst="LD0" prefix="" lnClass="XCBR" lnInst="1" doName="Pos" daName="stVal" fc="ST"/></DataSet>
        <GSEControl name="gcb1" datSet="gooseDs" confRev="1" appID="PROT1/LD0/gcb1"/>
      </LN0>
      <LN lnClass="PTOC" inst="1" lnType="PTOCt"/>
      <LN lnClass="PTRC" inst="1" lnType="PTRCt"/>
      <LN lnClass="XCBR" inst="1" lnType="XCBRt"/>
    </LDevice></Server></AccessPoint>
  </IED>
  <IED name="MU1">
    <AccessPoint name="P1"><Server><LDevice inst="LD0">
      <LN0 lnClass="LLN0" inst="" lnType="LLN0t">
        <DataSet name="svDs"><FCDA ldInst="LD0" lnClass="TCTR" lnInst="1" doName="Amp" daName="instMag.i" fc="MX"/></DataSet>
        <SampledValueControl name="msvcb1" datSet="svDs" confRev="1" smvID="MU01" smpRate="80" nofASDU="1"/>
      </LN0>
      <LN lnClass="TCTR" inst="1" lnType="TCTRt"/>
      <LN lnClass="TVTR" inst="1" lnType="TVTRt"/>
    </LDevice></Server></AccessPoint>
  </IED>
</SCL>
