from apsimNGpy.core.apsim import ApsimModel
from apsimNGpy.core.model_tools import ModelTools
import APSIM.Core as ApsimCore
from apsimNGpy.core.cs_resources import CastHelper
import Models
from System import DateTime

dt = DateTime(2000, 1, 1)
code  ="""
using Models.Soils;
using System;
using Models.Core;
using Models.PMF;
using APSIM.Shared.Utilities;
using Models.Surface;

namespace Models
{
    [Serializable]
    public class Script : Model
    {
        [Link] Clock Clock;
        [Link] SurfaceOrganicMatter SOM;
        [Link(IsOptional = true)] private IPlant existingCrop;
        [Link] ISummary Summary;
        [Separator("Applies tillage to an existing crop when it is ending")]
        //[Description("Crop")]
        //public IPlant Crop { get; set; }
        
        [Description("Fraction of Residues To Incorporate (0-1)")]
        public double Fraction { get; set; }
        
        [Description("Depth of Tillage (mm)")]
        public double Depth { get; set; }
        
        
        public enum ApplyTillage { yes, no }
        [Description("Do you want to till the land?")] 
        public ApplyTillage AppplyTillageOption { get; set; }

        [EventSubscribe("PlantEnding")]
        private void OnEndCrop(object sender, EventArgs e)
        {
            Model existingCrop = sender as Model;
            if (existingCrop != null && existingCrop.Name.ToLower() == (existingCrop as IModel).Name.ToLower()&& ApplyTillage.yes ==AppplyTillageOption)
            
            {
           
            SOM.Incorporate(Fraction, Depth);
            
           }
           
           
             Summary.WriteMessage(this, $"Tillage is applied to: {existingCrop.Name}", MessageType.Information);
        }
    }
}
"""
if __name__ == "__main__":
    with ApsimModel("Soybean") as model:
        # create a fresh simulation
        sim = Models.Core.Simulation()
        zone =Models.Core.Zone()
      # manager script
        manager =Models.Manager()
        manager.set_Code(code)
        manager.Rename('Tillage')
        manager.RebuildScriptModel()
        zone.Children.Add(manager)
        # clock
        clock = Models.Clock()
        clock.Start = dt
        clock.Start.AddYears(10)
        sim.AddChild(clock)
        crop = Models.PMF.Plant()
        crop.Name = 'Soybean'
        crop.ResourceName = 'Soybean'
        sim.AddChild(crop)
        sim.AddChild(zone)

        mock_sims = ApsimCore.Node.Create(Models.Core.Simulations())
        datastore = Models.Storage.DataStore()

        mock_sims.AddChild(sim)
        siM = CastHelper.CastAs[Models.Core.Simulations](mock_sims.Model)
        siM.Write('aps.apsimx')
        with ApsimModel('aps.apsimx') as ap:
            ap.inspect_file()


