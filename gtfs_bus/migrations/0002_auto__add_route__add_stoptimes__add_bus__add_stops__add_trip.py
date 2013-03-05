# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Route'
        db.create_table('gtfs_bus_route', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('route_id', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('route_shortname', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('route_long_name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('gtfs_bus', ['Route'])

        # Adding model 'StopTimes'
        db.create_table('gtfs_bus_stoptimes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trip', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs_bus.Trip'])),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs_bus.Stops'])),
            ('arrival_time', self.gf('django.db.models.fields.TimeField')()),
            ('departure_time', self.gf('django.db.models.fields.TimeField')()),
            ('stop_sequence', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('gtfs_bus', ['StopTimes'])

        # Adding model 'Bus'
        db.create_table('gtfs_bus_bus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trip', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs_bus.Trip'])),
            ('phone_num', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(max_digits=30, decimal_places=12)),
            ('lon', self.gf('django.db.models.fields.DecimalField')(max_digits=30, decimal_places=12)),
        ))
        db.send_create_signal('gtfs_bus', ['Bus'])

        # Adding model 'Stops'
        db.create_table('gtfs_bus_stops', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stop_name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('phone_num', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('stop_id', self.gf('django.db.models.fields.IntegerField')()),
            ('lat', self.gf('django.db.models.fields.DecimalField')(max_digits=30, decimal_places=12)),
            ('lon', self.gf('django.db.models.fields.DecimalField')(max_digits=30, decimal_places=12)),
            ('light_num', self.gf('django.db.models.fields.IntegerField')(blank=True)),
        ))
        db.send_create_signal('gtfs_bus', ['Stops'])

        # Adding model 'Trip'
        db.create_table('gtfs_bus_trip', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trip_id', self.gf('django.db.models.fields.IntegerField')()),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs_bus.Route'])),
            ('day', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('headsign', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('gtfs_bus', ['Trip'])


    def backwards(self, orm):
        # Deleting model 'Route'
        db.delete_table('gtfs_bus_route')

        # Deleting model 'StopTimes'
        db.delete_table('gtfs_bus_stoptimes')

        # Deleting model 'Bus'
        db.delete_table('gtfs_bus_bus')

        # Deleting model 'Stops'
        db.delete_table('gtfs_bus_stops')

        # Deleting model 'Trip'
        db.delete_table('gtfs_bus_trip')


    models = {
        'gtfs_bus.bus': {
            'Meta': {'object_name': 'Bus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '30', 'decimal_places': '12'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'max_digits': '30', 'decimal_places': '12'}),
            'phone_num': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'trip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs_bus.Trip']"})
        },
        'gtfs_bus.route': {
            'Meta': {'object_name': 'Route'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route_id': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'route_long_name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'route_shortname': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'gtfs_bus.stops': {
            'Meta': {'object_name': 'Stops'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '30', 'decimal_places': '12'}),
            'light_num': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'max_digits': '30', 'decimal_places': '12'}),
            'phone_num': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'stop_id': ('django.db.models.fields.IntegerField', [], {}),
            'stop_name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'gtfs_bus.stoptimes': {
            'Meta': {'object_name': 'StopTimes'},
            'arrival_time': ('django.db.models.fields.TimeField', [], {}),
            'departure_time': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs_bus.Stops']"}),
            'stop_sequence': ('django.db.models.fields.IntegerField', [], {}),
            'trip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs_bus.Trip']"})
        },
        'gtfs_bus.trip': {
            'Meta': {'object_name': 'Trip'},
            'day': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'headsign': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs_bus.Route']"}),
            'trip_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['gtfs_bus']