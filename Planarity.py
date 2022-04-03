#!/usr/bin/env python3

import tkinter as tk                    
from tkinter import ttk

import libPlanarity
import math
import numpy as np


class App( object ):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Planarity")
        self.tabControl = ttk.Notebook( self.root )

        self.tab_main = ttk.Frame( self.tabControl )
        self.tab_data = ttk.Frame( self.tabControl )
        self.tab_ref = ttk.Frame( self.tabControl )
        
        self.tabControl.add( self.tab_main, text ='Main')
        self.tabControl.add( self.tab_data, text ='Data')
        self.tabControl.add( self.tab_ref, text ='Reference')
        self.tabControl.pack(expand = 1, fill ="both")


        self.text_data = tk.Text( self.tab_data, height = 20, width = 35 )
        self.text_data.grid( row = 0, column = 0, padx = 10, pady = 10, columnspan=2 )
        ttk.Button( self.tab_data, text = "Load data from file", command = self.load_data_file ).grid( row = 1, column = 0, columnspan=2)

        self.text_ref = tk.Text( self.tab_ref, height = 20, width = 35 )
        self.text_ref.grid( row = 0, column = 0, padx = 10, pady = 10, columnspan=2 )
        ttk.Button( self.tab_ref, text = "Load reference from file", command = self.load_ref_file ).grid( row = 1, column = 0, columnspan=2)


        row = 0

        # Remove Z offset
        self.var_remove_z_offset = tk.IntVar()
        tk.Checkbutton( self.tab_main, text = "Remove Z offsets", variable=self.var_remove_z_offset, onvalue=1, offvalue=0 ).grid( row = row, column = 0, sticky = tk.W )
        row += 1

        # Use reference plane
        self.var_use_ref_plane = tk.IntVar()
        tk.Checkbutton( self.tab_main, text = "Use reference plane", variable=self.var_use_ref_plane, onvalue=1, offvalue=0 ).grid( row = row, column = 0, sticky = tk.W )
        row += 1

        # Show diff plane
        self.var_show_diff_plane = tk.IntVar()
        tk.Checkbutton( self.tab_main, text = "Show diff plane", variable=self.var_show_diff_plane, onvalue=1, offvalue=0 ).grid( row = row, column = 0, sticky = tk.W )
        row += 1

        # Show ref plane
        self.var_show_ref_plane = tk.IntVar()
        tk.Checkbutton( self.tab_main, text = "Show ref plane", variable=self.var_show_ref_plane, onvalue=1, offvalue=0 ).grid( row = row, column = 0, sticky = tk.W )
        row += 1


        tk.Label(self.tab_main, text = "Results" ).grid( row = row, column = 0, padx = 10, pady = 0, columnspan=2)
        row += 1
        self.text_main = tk.Text( self.tab_main, height = 15, width = 35 )
        self.text_main.grid( row = row, column = 0, padx = 10, pady = 10 , columnspan=2)
        row += 1
        ttk.Button( self.tab_main, text = "Compute", command = self.do_compute).grid( row = row, column = 0, padx = 5, pady = 5, columnspan=2  )


        self.print_ref( "# Default reference plane" )
        self.print_ref( "0 0 0" )
        self.print_ref( "1 0 0" )
        self.print_ref( "1 1 0" )

        self.print_main( "# Put some data to 'Data' tab.")
        self.print_data( "# Copy-paste data here.")
        self.print_data( "# Format: x y z")
        self.print_data( "# (in millimetres)")
        
        


    def print_main( self, *args ):
        line = " ".join([str(a) for a in args]) + "\n"
        self.text_main.insert( tk.END, line )

    def print_data( self, *args ):
        line = " ".join([str(a) for a in args]) + "\n"
        self.text_data.insert( tk.END, line )

    def print_ref( self, *args ):
        line = " ".join([str(a) for a in args]) + "\n"
        self.text_ref.insert( tk.END, line )

    def clear_main( self ):
        self.text_main.delete("1.0", tk.END )

    def clear_data( self ):
        self.text_data.delete("1.0", tk.END )
        
    def clear_ref( self ):
        self.text_ref.delete("1.0", tk.END )
        
    def parse_data( self ):
        txt = self.text_data.get("1.0", tk.END )
        lines = txt.splitlines(False)
        out = []
        for line in lines:
            line = line.strip()
            if len(line) < 1 or line.startswith("#"):
                continue
            out.append( [float(p) for p in line.split() ])
        return out

    def parse_ref( self ):
        txt = self.text_ref.get("1.0", tk.END )
        lines = txt.splitlines(False)
        out = []
        for line in lines:
            line = line.strip()
            if len(line) < 1 or line.startswith("#"):
                continue
            out.append( [float(p) for p in line.split() ])
        return out
    
    def do_compute( self ):
        ref_points = self.parse_ref()
        data_points = self.parse_data()
        
        removeZoffset = self.var_remove_z_offset.get() == 1
        
        ref_plane = libPlanarity.fit_plane( ref_points, removeOffset = removeZoffset )
        
        if self.var_use_ref_plane.get() > 0:
            # Remove reference plane from data before fitting
            data_plane = libPlanarity.fit_plane( libPlanarity.difference_from_plane( data_points, ref_plane["plane"] ), removeOffset = removeZoffset )
        else:
            data_plane = libPlanarity.fit_plane( data_points, removeOffset = removeZoffset )
        
        
        # How much points deviate from best fit plane
        diff_points = libPlanarity.difference_from_plane( data_plane["points"], data_plane["plane"] )
        diff_plane = libPlanarity.fit_plane( diff_points )

        max_error = max( [p[2] for p in diff_points ] )
        min_error = min( [p[2] for p in diff_points ] )
        std_error = np.std( [p[2] for p in diff_points ] )
        mad_error = np.mean( [abs(p[2]) for p in diff_points ] )

        self.clear_main()
        self.print_main( "Plane rotation:")
        self.print_main( "  X: %+.3f°, %+.3f µm/mm" % ( data_plane["euler"][0], 1000*math.tan( data_plane["euler"][0] * math.pi/180.0) ) )
        self.print_main( "  Y: %+.3f°, %+.3f µm/mm" % ( data_plane["euler"][1], 1000*math.tan( data_plane["euler"][1] * math.pi/180.0) ) )
        self.print_main( "")
        self.print_main( "Plane orientation:")
        self.print_main( "  Direction: %+.3f°" % data_plane["orient"][1] )
        self.print_main( "       Tilt: %+.3f°" % data_plane["orient"][0] )
        self.print_main( "")
        self.print_main( "Deviation from fitted plane:")
        self.print_main( "  Max: %+.3f mm" % max_error )
        self.print_main( "  Min: %+.3f mm" % min_error )
        self.print_main( "  RMS: %+.3f mm" % std_error )
        self.print_main( "  MAD: %+.3f mm" % mad_error )
        
        
        if self.var_show_diff_plane.get() == 1:
            if self.var_show_ref_plane.get() == 1:
                libPlanarity.plot_two_planes( diff_plane, ref_plane )
            else:
                libPlanarity.plot_plane( diff_plane )
        else:
            if self.var_show_ref_plane.get() == 1:
                libPlanarity.plot_two_planes( data_plane, ref_plane )
            else:
                libPlanarity.plot_plane( data_plane )
        
        
    def load_data_file( self ):
        fn = tk.filedialog.askopenfilename(initialdir = ".",title = "Select data file",filetypes = (("Text file","*.txt"),("All files","*.*")))
        if len(fn) > 0:
            self.clear_data()
            with open( fn, 'r' ) as handle:
                for line in handle:
                    self.print_data( line.strip() )
    
    def load_ref_file( self ):
        fn = tk.filedialog.askopenfilename(initialdir = ".",title = "Select reference file",filetypes = (("Text file","*.txt"),("All files","*.*")))
        if len(fn) > 0:
            self.clear_ref()
            with open( fn, 'r' ) as handle:
                for line in handle:
                    self.print_ref( line.strip() )
    


    def placeholder( self ):
        pass

    def run( self ):
        self.root.mainloop()




app = App()
app.run()